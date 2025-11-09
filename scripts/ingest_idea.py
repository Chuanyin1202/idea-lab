#!/usr/bin/env python3
"""
IdeaBrowser Idea Ingestion Script

從 Gmail API 抓取 IdeaBrowser 每日信件，
使用 OpenAI gpt-4o-mini 生成 PRD，
並寫入 ideas/ 目錄。

使用 OAuth 2.0 認證。
"""

import os
import json
import re
import sys
import time
import base64
import argparse
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path

# 載入環境變數（從 .env 檔案）
try:
    from dotenv import load_dotenv
    load_dotenv()  # 自動載入專案根目錄的 .env 檔案
except ImportError:
    pass  # 如果沒有安裝 python-dotenv，繼續執行（使用系統環境變數）

# 需要安裝的套件：
# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client openai python-dotenv requests beautifulsoup4 lxml

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import openai
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"❌ 缺少必要套件: {e}")
    print("請執行: pip install -r requirements.txt")
    sys.exit(1)


# ==================== 設定 ====================

GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
IDEABROWSER_FROM = 'notifications@mail.ideabrowser.com'
IDEABROWSER_SUBJECT = 'Idea of the Day'

# 檔案路徑
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CREDENTIALS_FILE = PROJECT_ROOT / 'credentials.json'
TOKEN_FILE = PROJECT_ROOT / 'token.json'

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


# ==================== OAuth 2.0 認證 ====================

def get_credentials(force_reauth: bool = False) -> Credentials:
    """
    取得 Gmail API credentials

    Args:
        force_reauth: 強制重新授權

    Returns:
        Google OAuth 2.0 credentials
    """
    creds = None

    # 嘗試從 token.json 載入
    if TOKEN_FILE.exists() and not force_reauth:
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), GMAIL_SCOPES)
            log(f"✅ 從 token.json 載入憑證")
        except Exception as e:
            log(f"⚠️  載入 token.json 失敗: {e}")
            creds = None

    # 如果憑證不存在或失效，嘗試更新
    if creds and creds.expired and creds.refresh_token:
        try:
            log("🔄 Token 已過期，嘗試更新...")
            creds.refresh(Request())
            log("✅ Token 更新成功")
        except Exception as e:
            log(f"❌ Token 更新失敗: {e}")
            creds = None

    # 如果仍無有效憑證，執行 OAuth flow
    if not creds or not creds.valid:
        if not CREDENTIALS_FILE.exists():
            log(f"❌ 找不到 credentials.json: {CREDENTIALS_FILE}")
            log("請先設定 OAuth 2.0 憑證")
            sys.exit(1)

        try:
            log("🔐 啟動 OAuth 2.0 授權流程...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), GMAIL_SCOPES
            )

            # 嘗試使用本機伺服器（適合桌面環境）
            try:
                creds = flow.run_local_server(port=0)
                log("✅ 授權成功（本機伺服器模式）")
            except Exception as e:
                # 如果失敗，使用 console 模式（適合無頭環境）
                log(f"⚠️  本機伺服器模式失敗: {e}")
                log("🔄 切換到 console 模式...")
                creds = flow.run_console()
                log("✅ 授權成功（console 模式）")

        except Exception as e:
            log(f"❌ OAuth 授權失敗: {e}")
            sys.exit(1)

        # 儲存 token 供下次使用
        try:
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
            log(f"✅ Token 已儲存到: {TOKEN_FILE}")
        except Exception as e:
            log(f"⚠️  無法儲存 token: {e}")

    return creds


def load_credentials_from_env() -> Credentials:
    """
    從環境變數載入憑證（適合 GitHub Actions）

    環境變數：
    - GMAIL_TOKEN_JSON: token.json 的 Base64 編碼內容
    """
    token_b64 = os.getenv('GMAIL_TOKEN_JSON')

    if not token_b64:
        log("❌ 找不到環境變數 GMAIL_TOKEN_JSON")
        log("請在 GitHub Secrets 中設定此變數")
        sys.exit(1)

    try:
        token_json = base64.b64decode(token_b64).decode('utf-8')
        token_data = json.loads(token_json)
        creds = Credentials.from_authorized_user_info(token_data, GMAIL_SCOPES)
        log("✅ 從環境變數載入憑證")
        return creds
    except Exception as e:
        log(f"❌ 解析環境變數憑證失敗: {e}")
        sys.exit(1)


def get_gmail_service(use_env: bool = False, force_reauth: bool = False):
    """
    建立 Gmail API service

    Args:
        use_env: 是否從環境變數讀取（GitHub Actions 模式）
        force_reauth: 強制重新授權
    """
    if use_env:
        creds = load_credentials_from_env()
    else:
        creds = get_credentials(force_reauth)

    service = build('gmail', 'v1', credentials=creds)
    return service


# ==================== Gmail API 搜尋 ====================

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


def extract_url_from_email(email_body: str) -> Optional[str]:
    """
    從 email body 中提取 IdeaBrowser 完整分析的 URL

    Args:
        email_body: email 內容

    Returns:
        URL 字串或 None
    """
    # 尋找 https://www.ideabrowser.com/idea/... 格式的 URL
    url_pattern = r'https://www\.ideabrowser\.com/idea/[a-zA-Z0-9\-]+'

    match = re.search(url_pattern, email_body)
    if match:
        return match.group(0)

    return None


def fetch_full_idea_analysis(url: str, timeout: int = 10) -> Optional[str]:
    """
    抓取 IdeaBrowser 網頁的完整分析內容

    Args:
        url: IdeaBrowser idea 頁面 URL
        timeout: 請求超時時間（秒）

    Returns:
        網頁文字內容或 None
    """
    try:
        log(f"🌐 抓取完整分析: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        # 移除 script 和 style 標籤
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()

        # 提取主要內容
        # 優先尋找 article、main 或 content 相關的 div
        main_content = (
            soup.find('article') or
            soup.find('main') or
            soup.find('div', class_=re.compile(r'content|article|post', re.I))
        )

        if main_content:
            text = main_content.get_text(separator='\n', strip=True)
        else:
            # 降級為整個 body
            text = soup.body.get_text(separator='\n', strip=True) if soup.body else soup.get_text(separator='\n', strip=True)

        # 清理多餘空行
        text = re.sub(r'\n\s*\n+', '\n\n', text)

        log(f"✅ 抓取成功 (長度: {len(text)} 字元)")
        return text

    except requests.Timeout:
        log(f"⚠️  請求超時 ({timeout}秒)")
        return None
    except requests.RequestException as e:
        log(f"⚠️  網路請求失敗: {e}")
        return None
    except Exception as e:
        log(f"⚠️  解析網頁失敗: {e}")
        return None


# ==================== OpenAI API ====================

def generate_prd_with_openai(email_summary: str, full_analysis: Optional[str] = None, retry: int = 0) -> Optional[str]:
    """
    使用 OpenAI gpt-4o-mini 生成 PRD

    Args:
        email_summary: 從 email 提取的摘要內容
        full_analysis: 從網頁抓取的完整分析（可選）
        retry: 當前重試次數

    Returns:
        生成的 PRD Markdown 或 None
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        log("❌ 找不到 OPENAI_API_KEY 環境變數")
        return None

    client = openai.OpenAI(api_key=api_key)

    # 組合內容
    if full_analysis:
        idea_content = f"""**Email 摘要**:
{email_summary}

---

**完整分析**:
{full_analysis}
"""
    else:
        idea_content = email_summary

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
- 如果提供了完整分析，請充分利用其中的市場洞察、競品分析、技術建議等資訊

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
            return generate_prd_with_openai(email_summary, full_analysis, retry + 1)
        return None

    except openai.APIError as e:
        log(f"❌ OpenAI API 錯誤: {e}")
        if retry < MAX_RETRIES_OPENAI:
            log(f"   {RETRY_DELAY} 秒後重試...")
            time.sleep(RETRY_DELAY)
            return generate_prd_with_openai(email_summary, full_analysis, retry + 1)
        return None

    except Exception as e:
        log(f"❌ 生成 PRD 時發生錯誤: {e}")
        return None


# ==================== 檔案操作 ====================

def extract_metadata_from_content(content: str, email_data: Dict[str, Any]) -> Dict[str, Any]:
    """從信件內容和 PRD 中提取 metadata"""

    # 從 PRD 中提取產品名稱
    title = "Untitled Idea"

    # 方法 1：從 "## 產品名稱" 區塊提取
    product_name_match = re.search(r'##\s*產品名稱\s*\n\s*(.+)', content, re.MULTILINE)
    if product_name_match:
        title = product_name_match.group(1).strip()
    else:
        # 方法 2：從第一行提取（回退方案）
        first_line = content.split('\n')[0]
        title_match = re.search(r'#\s*(.+)', first_line)
        if title_match:
            title = title_match.group(1).strip()
            # 排除通用標題
            if title in ['產品需求文件 (PRD)', 'PRD', 'Product Requirements Document']:
                title = "Untitled Idea"

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
    parser = argparse.ArgumentParser(description='IdeaBrowser Idea Ingestion Script')
    parser.add_argument('--auth', action='store_true', help='執行 OAuth 授權流程')
    parser.add_argument('--reauth', action='store_true', help='強制重新授權')
    parser.add_argument('--env', action='store_true', help='從環境變數讀取憑證（GitHub Actions 模式）')
    args = parser.parse_args()

    log("=" * 60)
    log("🚀 IdeaBrowser Idea Ingestion Script")
    log("=" * 60)

    # 如果只是授權，執行後結束
    if args.auth or args.reauth:
        log("\n🔐 執行 OAuth 2.0 授權...")
        try:
            get_credentials(force_reauth=True)
            log("\n✅ 授權完成！")
            log(f"Token 已儲存到: {TOKEN_FILE}")
            log("\n下次執行時將自動使用此 token")
        except Exception as e:
            log(f"\n❌ 授權失敗: {e}")
            sys.exit(1)
        return

    # 1. 連接 Gmail API
    log("\n📬 Step 1: 連接 Gmail API")
    try:
        gmail_service = get_gmail_service(use_env=args.env)
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

    # 3. 抓取完整分析（如果有 URL）
    log("\n🌐 Step 3: 抓取完整分析")
    full_analysis = None
    url = extract_url_from_email(email_data['body'])

    if url:
        log(f"   找到 URL: {url}")
        full_analysis = fetch_full_idea_analysis(url)

        if not full_analysis:
            log("   ⚠️  網頁抓取失敗，將只使用 email 摘要")
    else:
        log("   ⚠️  Email 中沒有找到 URL，將只使用 email 摘要")

    # 4. 生成 PRD
    log("\n🤖 Step 4: 使用 OpenAI 生成 PRD")
    prd = generate_prd_with_openai(email_data['body'], full_analysis)

    if not prd:
        log("\n❌ PRD 生成失敗")
        sys.exit(1)

    # 5. 寫入檔案
    log("\n💾 Step 5: 寫入檔案")
    success = write_idea_files(prd, email_data)

    if not success:
        log("\n⚠️  檔案寫入失敗或已存在")
        sys.exit(0)

    log("\n" + "=" * 60)
    log("✅ 完成！")
    log("=" * 60)


if __name__ == "__main__":
    main()
