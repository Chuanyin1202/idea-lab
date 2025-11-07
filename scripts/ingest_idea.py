#!/usr/bin/env python3
"""
IdeaBrowser Idea Ingestion Script

從 Gmail API 抓取 IdeaBrowser 每日信件，
使用 OpenAI gpt-4o-mini 生成 PRD，
並寫入 ideas/ 目錄。
"""

import os
import json
import re
import sys
import time
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# 需要安裝的套件：
# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client openai

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import openai
except ImportError as e:
    print(f"❌ 缺少必要套件: {e}")
    print("請執行: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client openai")
    sys.exit(1)


# ==================== 設定 ====================

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
IDEABROWSER_FROM = 'ideas@ideabrowser.com'  # 請根據實際寄件者調整
IDEABROWSER_SUBJECT = 'Idea of the Day'      # 請根據實際主旨調整

# OpenAI 設定
OPENAI_MODEL = 'gpt-4o-mini'
OPENAI_TEMPERATURE = 0.4
OPENAI_MAX_TOKENS = 4000

# 重試設定
MAX_RETRIES_GMAIL = 3
MAX_RETRIES_OPENAI = 2
RETRY_DELAY = 5  # 秒


# ==================== 工具函式 ====================

def slugify(text: str) -> str:
    """將文字轉換為適合檔名的 slug"""
    s = re.sub(r'[^a-zA-Z0-9]+', '-', text).strip('-').lower()
    return s[:50] or "idea"  # 限制長度


def today_str() -> str:
    """取得今天日期字串 (YYYY-MM-DD)"""
    return datetime.utcnow().strftime("%Y-%m-%d")


def ensure_dir(path: str):
    """確保目錄存在"""
    os.makedirs(path, exist_ok=True)


def log(msg: str):
    """帶時間戳記的日誌"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")


# ==================== Gmail API ====================

def get_gmail_service():
    """
    建立 Gmail API service

    需要環境變數：
    - GOOGLE_APPLICATION_CREDENTIALS: Service Account JSON 檔案路徑
    或
    - GOOGLE_SERVICE_ACCOUNT_JSON: Service Account JSON 內容（Base64 編碼）
    """
    creds = None

    # 方案 1: 從檔案讀取
    creds_file = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if creds_file and os.path.exists(creds_file):
        creds = service_account.Credentials.from_service_account_file(
            creds_file, scopes=GMAIL_SCOPES
        )
        log(f"✅ 從檔案載入 Service Account: {creds_file}")

    # 方案 2: 從環境變數讀取 JSON（適合 GitHub Actions）
    elif os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'):
        try:
            json_str = base64.b64decode(os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')).decode('utf-8')
            info = json.loads(json_str)
            creds = service_account.Credentials.from_service_account_info(
                info, scopes=GMAIL_SCOPES
            )
            log("✅ 從環境變數載入 Service Account")
        except Exception as e:
            log(f"❌ 解析 GOOGLE_SERVICE_ACCOUNT_JSON 失敗: {e}")
            raise

    else:
        log("❌ 找不到 Google Service Account 認證")
        log("請設定環境變數：")
        log("  - GOOGLE_APPLICATION_CREDENTIALS (檔案路徑)")
        log("  - GOOGLE_SERVICE_ACCOUNT_JSON (Base64 編碼的 JSON)")
        sys.exit(1)

    # 如果需要 domain-wide delegation，加上這行：
    # delegated_email = 'your-email@gmail.com'
    # creds = creds.with_subject(delegated_email)

    service = build('gmail', 'v1', credentials=creds)
    return service


def search_ideabrowser_email(service, days_ago: int = 1) -> Optional[Dict[str, Any]]:
    """
    搜尋 IdeaBrowser 信件

    Args:
        service: Gmail API service
        days_ago: 搜尋幾天前的信件

    Returns:
        信件內容 dict 或 None
    """
    try:
        # 建立搜尋條件
        after_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y/%m/%d")
        query = f'from:{IDEABROWSER_FROM} subject:"{IDEABROWSER_SUBJECT}" after:{after_date}'

        log(f"🔍 搜尋條件: {query}")

        # 搜尋信件
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=1
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            log(f"📭 找不到符合條件的信件")
            return None

        # 取得完整信件內容
        msg_id = messages[0]['id']
        message = service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()

        log(f"📧 找到信件 ID: {msg_id}")

        # 解析信件
        payload = message['payload']
        headers = {h['name']: h['value'] for h in payload['headers']}

        subject = headers.get('Subject', '')
        from_email = headers.get('From', '')
        date = headers.get('Date', '')

        log(f"   主旨: {subject}")
        log(f"   寄件者: {from_email}")
        log(f"   日期: {date}")

        # 取得信件內容（支援 plain text 和 HTML）
        body = extract_email_body(payload)

        if not body:
            log("⚠️  無法解析信件內容")
            return None

        return {
            'subject': subject,
            'from': from_email,
            'date': date,
            'body': body,
            'message_id': msg_id
        }

    except HttpError as e:
        log(f"❌ Gmail API 錯誤: {e}")
        return None
    except Exception as e:
        log(f"❌ 搜尋信件時發生錯誤: {e}")
        return None


def extract_email_body(payload) -> str:
    """從信件 payload 中提取內容"""
    body = ""

    # 單一 part（plain text）
    if 'body' in payload and 'data' in payload['body']:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

    # 多 part（可能有 HTML 和 plain text）
    elif 'parts' in payload:
        for part in payload['parts']:
            mime_type = part.get('mimeType', '')

            # 優先使用 plain text
            if mime_type == 'text/plain' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break

            # 備用：使用 HTML（需要額外處理）
            elif mime_type == 'text/html' and 'data' in part['body']:
                html = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                # 簡單的 HTML 轉純文字（可改用 BeautifulSoup）
                body = re.sub(r'<[^>]+>', '', html)

    return body.strip()


# ==================== OpenAI API ====================

def generate_prd_with_openai(idea_content: str, retry: int = 0) -> Optional[str]:
    """
    使用 OpenAI gpt-4o-mini 生成 PRD

    Args:
        idea_content: 從信件提取的 idea 內容
        retry: 當前重試次數

    Returns:
        生成的 PRD Markdown 或 None
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        log("❌ 找不到 OPENAI_API_KEY 環境變數")
        return None

    client = openai.OpenAI(api_key=api_key)

    prompt = f"""你是一位資深產品經理。

請根據以下創業點子，撰寫一份完整的產品需求文件（PRD）。

**輸出格式**: 純 Markdown

**必須包含的章節**:
1. 產品名稱
2. One-line Pitch
3. Background & Problem Statement
4. Target Users & Personas
5. User Pain Points
6. Value Proposition
7. Core Use Cases & User Stories
8. MVP Scope (Must-have vs Nice-to-have)
9. User Flow Overview
10. Basic System Architecture
11. Monetization Hypothesis
12. Success Metrics
13. Risks & Assumptions

**注意事項**:
- 使用繁體中文撰寫
- 內容具體、可執行
- MVP Scope 要明確區分 Must-have 和 Nice-to-have
- System Architecture 要包含技術棧建議

---

**Idea 內容**:
{idea_content}

請開始撰寫 PRD:
"""

    try:
        log(f"🤖 呼叫 OpenAI API (model: {OPENAI_MODEL}, retry: {retry}/{MAX_RETRIES_OPENAI})")

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "你是一位經驗豐富的產品經理，擅長撰寫清晰、可執行的產品需求文件。"},
                {"role": "user", "content": prompt}
            ],
            temperature=OPENAI_TEMPERATURE,
            max_tokens=OPENAI_MAX_TOKENS,
        )

        prd = response.choices[0].message.content.strip()

        log(f"✅ PRD 生成完成 (長度: {len(prd)} 字元)")
        log(f"   使用 tokens: {response.usage.total_tokens}")

        return prd

    except openai.RateLimitError as e:
        log(f"⚠️  OpenAI API 達到速率限制: {e}")
        if retry < MAX_RETRIES_OPENAI:
            log(f"   {RETRY_DELAY} 秒後重試...")
            time.sleep(RETRY_DELAY)
            return generate_prd_with_openai(idea_content, retry + 1)
        return None

    except openai.APIError as e:
        log(f"❌ OpenAI API 錯誤: {e}")
        if retry < MAX_RETRIES_OPENAI:
            log(f"   {RETRY_DELAY} 秒後重試...")
            time.sleep(RETRY_DELAY)
            return generate_prd_with_openai(idea_content, retry + 1)
        return None

    except Exception as e:
        log(f"❌ 生成 PRD 時發生錯誤: {e}")
        return None


# ==================== 檔案操作 ====================

def extract_metadata_from_content(content: str, email_data: Dict[str, Any]) -> Dict[str, Any]:
    """從信件內容和 PRD 中提取 metadata"""

    # 從 PRD 第一行提取產品名稱
    first_line = content.split('\n')[0]
    title_match = re.search(r'#\s*(.+)', first_line)
    title = title_match.group(1).strip() if title_match else "Untitled Idea"

    # 嘗試從內容中提取分類和標籤（簡單版本）
    category = "general"
    tags = ["mvp", "saas"]

    # 可以根據內容關鍵字自動分類
    content_lower = content.lower()
    if any(word in content_lower for word in ['esports', 'gaming', 'tournament']):
        category = "esports"
        tags.append("gaming")
    elif any(word in content_lower for word in ['ai', 'machine learning', 'llm']):
        category = "ai"
        tags.append("ai")
    elif any(word in content_lower for word in ['saas', 'platform', 'tool']):
        category = "saas"
        tags.append("automation")

    return {
        "date": today_str(),
        "title": title,
        "source": "ideabrowser",
        "email_id": email_data.get('message_id'),
        "category": category,
        "tags": tags,
        "status": "new"
    }


def write_idea_files(prd: str, email_data: Dict[str, Any]) -> bool:
    """
    將 PRD 和 metadata 寫入檔案

    Returns:
        是否成功寫入
    """
    try:
        # 提取 metadata
        meta = extract_metadata_from_content(prd, email_data)

        # 建立目錄
        date_str = meta['date']
        slug = slugify(meta['title'])
        base_dir = f"ideas/{date_str}-{slug}"

        # 檢查是否已存在
        if os.path.exists(base_dir):
            log(f"⚠️  目錄已存在: {base_dir}")
            log(f"   跳過以避免覆蓋")
            return False

        ensure_dir(base_dir)
        log(f"📁 建立目錄: {base_dir}")

        # 寫入 PRD.md
        prd_path = f"{base_dir}/PRD.md"
        with open(prd_path, "w", encoding="utf-8") as f:
            f.write(prd)
        log(f"✍️  寫入 PRD: {prd_path}")

        # 寫入 meta.json
        meta_path = f"{base_dir}/meta.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        log(f"✍️  寫入 metadata: {meta_path}")

        # 更新 SUMMARY.md
        update_summary(meta, base_dir)

        log(f"✅ 成功新增 idea: {meta['title']}")
        return True

    except Exception as e:
        log(f"❌ 寫入檔案時發生錯誤: {e}")
        return False


def update_summary(meta: Dict[str, Any], idea_path: str):
    """更新 SUMMARY.md"""
    summary_path = "SUMMARY.md"

    # 如果檔案不存在，建立標題列
    if not os.path.exists(summary_path):
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("# Idea Summary\n\n")
            f.write("| Date       | Title | Category | Tags |\n")
            f.write("|------------|-------|----------|------|\n")
        log(f"📝 建立 SUMMARY.md")

    # 新增一行
    tags_str = ", ".join(meta["tags"])
    prd_link = f"{idea_path}/PRD.md"
    line = f"| {meta['date']} | [{meta['title']}]({prd_link}) | {meta['category']} | {tags_str} |\n"

    with open(summary_path, "a", encoding="utf-8") as f:
        f.write(line)

    log(f"📝 更新 SUMMARY.md")


# ==================== 主流程 ====================

def main():
    """主流程"""
    log("=" * 60)
    log("🚀 IdeaBrowser Idea Ingestion Script")
    log("=" * 60)

    # 1. 連接 Gmail API
    log("\n📬 Step 1: 連接 Gmail API")
    try:
        gmail_service = get_gmail_service()
    except Exception as e:
        log(f"❌ 無法建立 Gmail service: {e}")
        sys.exit(1)

    # 2. 搜尋今天的信件
    log("\n🔍 Step 2: 搜尋 IdeaBrowser 信件")
    email_data = None

    # 嘗試搜尋今天和昨天的信件（處理時區問題）
    for days_ago in [0, 1]:
        email_data = search_ideabrowser_email(gmail_service, days_ago)
        if email_data:
            break

    if not email_data:
        log("\n❌ 找不到 IdeaBrowser 信件")
        log("可能原因：")
        log("  1. 今天還沒收到信")
        log("  2. 信件主旨或寄件者不符")
        log("  3. Gmail API 權限不足")
        sys.exit(0)  # 不算錯誤，只是沒有新 idea

    # 3. 生成 PRD
    log("\n🤖 Step 3: 使用 OpenAI 生成 PRD")
    prd = generate_prd_with_openai(email_data['body'])

    if not prd:
        log("\n❌ PRD 生成失敗")
        sys.exit(1)

    # 4. 寫入檔案
    log("\n💾 Step 4: 寫入檔案")
    success = write_idea_files(prd, email_data)

    if not success:
        log("\n⚠️  檔案寫入失敗或已存在")
        sys.exit(0)

    log("\n" + "=" * 60)
    log("✅ 完成！")
    log("=" * 60)


if __name__ == "__main__":
    main()
