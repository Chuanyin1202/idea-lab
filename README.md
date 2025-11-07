# 💡 Idea Lab

個人 Idea / MVP 孵化實驗室。每天自動從 IdeaBrowser 收集創業點子，用 AI 生成完整的 PRD，方便隨時挑選實作。

## 🎯 核心概念

```
IdeaBrowser 每日信件
    ↓ (Gmail API)
OpenAI gpt-4o-mini 生成 PRD
    ↓
存入 ideas/ 目錄
    ↓
人類挑選喜歡的點子
    ↓
在 projects/ 實作 MVP
```

## 📁 目錄結構

```
idea-lab/
├── ideas/                    # 自動收集的 ideas
│   └── 2025-11-07-esports-tourneyflow/
│       ├── PRD.md           # 完整產品需求文件
│       └── meta.json        # 結構化資訊
├── projects/                 # 實作中的 MVP 專案
│   └── (專案目錄)
├── scripts/
│   └── ingest_idea.py       # 自動化腳本
├── SUMMARY.md               # Idea 索引表
└── .github/workflows/
    └── ingest_idea.yml      # GitHub Actions 設定
```

## 🚀 快速開始

### 1. 設定 Gmail API

#### 步驟 1: 建立 Google Cloud Project

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案（或使用現有專案）
3. 啟用 **Gmail API**

#### 步驟 2: 建立 Service Account

1. 前往 **IAM & Admin** > **Service Accounts**
2. 點擊 **Create Service Account**
3. 填寫名稱，例如：`ideabrowser-reader`
4. 點擊 **Create and Continue**
5. 不需要設定角色，直接點擊 **Done**

#### 步驟 3: 建立金鑰

1. 點擊剛建立的 Service Account
2. 前往 **Keys** 頁籤
3. 點擊 **Add Key** > **Create new key**
4. 選擇 **JSON** 格式
5. 下載 JSON 檔案（妥善保管，不要上傳到 Git）

#### 步驟 4: 設定 Domain-Wide Delegation（如果使用企業 Google Workspace）

如果你的 Gmail 是企業帳號，需要設定 Domain-Wide Delegation：

1. 在 Service Account 詳細頁面，啟用 **Enable Google Workspace Domain-wide Delegation**
2. 記下 **Client ID**
3. 前往 [Google Workspace Admin](https://admin.google.com/)
4. **Security** > **API Controls** > **Domain-wide Delegation**
5. 新增 Client ID，設定 OAuth Scopes：
   ```
   https://www.googleapis.com/auth/gmail.readonly
   ```

**個人 Gmail 帳號**可以跳過此步驟，直接使用 OAuth 2.0 登入。

### 2. 設定 GitHub Secrets

前往 GitHub repo > **Settings** > **Secrets and variables** > **Actions**，新增以下 secrets：

#### 必要 Secrets

| Secret 名稱 | 說明 | 如何取得 |
|------------|------|---------|
| `OPENAI_API_KEY` | OpenAI API 金鑰 | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Service Account JSON (Base64) | 見下方說明 |

#### 產生 `GOOGLE_SERVICE_ACCOUNT_JSON`

在本機執行：

```bash
# macOS / Linux
base64 -i path/to/service-account.json | pbcopy

# 或直接輸出到檔案
base64 -i path/to/service-account.json > encoded.txt
```

將 Base64 編碼後的內容貼到 GitHub Secret。

### 3. 調整信件搜尋條件

編輯 `scripts/ingest_idea.py`，修改以下變數：

```python
IDEABROWSER_FROM = 'ideas@ideabrowser.com'  # 寄件者 email
IDEABROWSER_SUBJECT = 'Idea of the Day'      # 信件主旨
```

根據你實際收到的 IdeaBrowser 信件調整。

### 4. 測試執行

#### 本機測試

```bash
# 1. 建立虛擬環境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 設定環境變數
export OPENAI_API_KEY="sk-..."
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

# 4. 執行腳本
python scripts/ingest_idea.py
```

#### GitHub Actions 測試

1. 前往 repo 的 **Actions** 頁面
2. 選擇 **Ingest IdeaBrowser Idea** workflow
3. 點擊 **Run workflow**
4. 查看執行結果

### 5. 啟用自動執行

預設每日 UTC 02:00（台灣時間 10:00）自動執行。

如需調整時間，編輯 `.github/workflows/ingest_idea.yml`：

```yaml
on:
  schedule:
    - cron: "0 2 * * *"  # 修改這裡
```

Cron 格式：`分 時 日 月 星期`

## 📖 使用流程

### 瀏覽 Ideas

開啟 [`SUMMARY.md`](SUMMARY.md) 查看所有收集的 ideas：

| Date       | Title                                                | Category | Tags                          |
|------------|------------------------------------------------------|----------|-------------------------------|
| 2025-11-07 | [TourneyFlow - Esports tournament management tool](ideas/2025-11-07-esports-tourneyflow/PRD.md) | esports  | mvp, saas, automation, discord |

### 查看完整 PRD

點擊連結查看完整的產品需求文件。

### 決定實作

如果某個 idea 值得實作：

```bash
# 1. 在 projects/ 建立專案目錄
mkdir -p projects/tourneyflow

# 2. 建立 README 標註來源
echo "# TourneyFlow

Source Idea: [2025-11-07-esports-tourneyflow](../../ideas/2025-11-07-esports-tourneyflow/PRD.md)
" > projects/tourneyflow/README.md

# 3. 開始實作（可以請 Claude Code 幫忙）
cd projects/tourneyflow
```

### 請 AI 協助實作

在專案目錄中：

```bash
# 用 Claude Code
claude "根據 ../../ideas/2025-11-07-esports-tourneyflow/PRD.md 建立 Next.js 專案骨架"
```

或直接給 AI 看 PRD：

> 嗨 Claude，我想實作這個 idea：
>
> [貼上 PRD 內容]
>
> 請幫我建立 Next.js + Tailwind 專案，並實作核心功能。

## 🛠 技術架構

### 自動化流程

- **觸發方式**: GitHub Actions (Cron Schedule)
- **執行環境**: Ubuntu Latest
- **Python 版本**: 3.11

### Gmail API

- **認證方式**: Service Account with OAuth 2.0
- **權限**: `gmail.readonly`
- **搜尋條件**:
  ```python
  from:{IDEABROWSER_FROM}
  subject:"{IDEABROWSER_SUBJECT}"
  after:{yesterday}
  ```

### OpenAI API

- **Model**: `gpt-4o-mini`
- **Temperature**: 0.4（保持一致性）
- **Max Tokens**: 4000
- **成本**: 約 $0.015/request，每月 < $1

### 錯誤處理

- Gmail API: 重試 3 次，間隔 5 秒
- OpenAI API: 重試 2 次，間隔 5 秒
- 失敗時輸出詳細錯誤訊息

## 🔧 進階設定

### 自訂 PRD 格式

編輯 `scripts/ingest_idea.py` 中的 `generate_prd_with_openai()` 函式，修改 prompt：

```python
prompt = f"""你是一位資深產品經理。

請根據以下創業點子，撰寫一份完整的產品需求文件（PRD）。

**你的自訂格式**...
"""
```

### 自動分類

在 `extract_metadata_from_content()` 中新增分類邏輯：

```python
if any(word in content_lower for word in ['blockchain', 'web3', 'nft']):
    category = "web3"
    tags.append("blockchain")
```

### 新增通知

在 workflow 中加入 Discord / Slack 通知：

```yaml
- name: Notify on success
  if: success()
  run: |
    curl -X POST ${{ secrets.DISCORD_WEBHOOK_URL }} \
      -H "Content-Type: application/json" \
      -d '{"content": "✅ 新增了一個 idea！"}'
```

## 🤔 常見問題

### Q: Gmail API 一直失敗？

**A**: 檢查：
1. Service Account JSON 是否正確？
2. Gmail API 是否已啟用？
3. 如果是企業帳號，是否設定 Domain-Wide Delegation？
4. 信件寄件者和主旨是否正確？

### Q: OpenAI API 超過額度？

**A**:
1. 檢查 [OpenAI 用量頁面](https://platform.openai.com/usage)
2. 考慮使用 `gpt-3.5-turbo`（更便宜）
3. 調整 `MAX_TOKENS` 降低成本

### Q: 想要手動新增 idea？

**A**: 直接在 `ideas/` 建立目錄和檔案：

```bash
mkdir -p ideas/2025-11-08-my-idea
echo "# My Idea" > ideas/2025-11-08-my-idea/PRD.md
echo '{"date": "2025-11-08", ...}' > ideas/2025-11-08-my-idea/meta.json
```

### Q: 能否支援其他來源（不只 IdeaBrowser）？

**A**: 可以！修改 `scripts/ingest_idea.py` 中的 `search_ideabrowser_email()` 函式，改成：
- RSS feed 解析
- Twitter / X 爬蟲
- Notion / Obsidian 筆記同步
- 其他 email 來源

## 📚 相關資源

- [ARCHITECTURE.md](ARCHITECTURE.md) - 詳細架構說明
- [Gmail API 文件](https://developers.google.com/gmail/api)
- [OpenAI API 文件](https://platform.openai.com/docs)
- [GitHub Actions 文件](https://docs.github.com/en/actions)

## 📝 授權

MIT License

---

**Made with ❤️ by Alex Huang**

Auto-collecting ideas, one PRD at a time.
