# 💡 Idea Lab

個人 Idea / MVP 孵化實驗室。每天自動從 IdeaBrowser 收集創業點子，用 AI 生成完整的 PRD，方便隨時挑選實作。

## 🎯 核心概念

```
IdeaBrowser 每日信件（trigger）
    ↓ (Gmail API)
抓取 IdeaBrowser 首頁完整內容
    ↓ (BeautifulSoup)
OpenAI gpt-4o-mini 生成 PRD
    ↓
自動 commit & push 到 GitHub
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

### 1. 設定 Gmail API (OAuth 2.0)

#### 步驟 1: 建立 Google Cloud Project

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案（或使用現有專案）
3. 啟用 **Gmail API**：
   - 在左側選單選擇「API 和服務」>「資料庫」
   - 搜尋「Gmail API」並啟用

#### 步驟 2: 建立 OAuth 2.0 憑證

1. 前往 **API 和服務** > **憑證**
2. 點擊 **建立憑證** > **OAuth 用戶端 ID**
3. 如果是第一次，需要先設定「OAuth 同意畫面」：
   - 選擇「外部」（個人帳號）或「內部」（企業帳號）
   - 填寫應用程式名稱（例如：Idea Lab）
   - 加入測試使用者（填入你的 Gmail）
4. 回到「憑證」頁面，建立 OAuth 用戶端 ID：
   - 應用程式類型：**電腦版應用程式**
   - 名稱：`idea-lab` 或任意名稱
5. 下載 JSON 檔案，重新命名為 `credentials.json`
6. 將 `credentials.json` 放到專案根目錄（**不要上傳到 Git**）

#### 步驟 3: 本機授權取得 Token

```bash
# 1. 建立虛擬環境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 執行授權流程
python scripts/ingest_idea.py --auth
```

瀏覽器會自動開啟 Google 授權頁面：
- 登入你的 Gmail 帳號
- 允許存取（readonly 權限）
- 授權成功後會產生 `token.json`

### 2. 設定 GitHub Secrets

前往 GitHub repo > **Settings** > **Secrets and variables** > **Actions**，新增以下 secrets：

#### 必要 Secrets

| Secret 名稱 | 說明 | 如何取得 |
|------------|------|---------|
| `OPENAI_API_KEY` | OpenAI API 金鑰 | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| `GMAIL_TOKEN_JSON` | Gmail OAuth Token (Base64) | 見下方說明 |

#### 產生 `GMAIL_TOKEN_JSON`

完成步驟 1-3 授權後，專案根目錄會有 `token.json`。在本機執行：

```bash
# macOS / Linux
base64 -i token.json | pbcopy

# 或直接輸出
base64 -i token.json > encoded.txt
```

將 Base64 編碼後的內容貼到 GitHub Secret `GMAIL_TOKEN_JSON`。

### 3. 測試執行

#### 本機測試

```bash
# 確保已授權（有 token.json）
source venv/bin/activate

# 設定 OpenAI API Key
export OPENAI_API_KEY="sk-..."

# 執行腳本
python scripts/ingest_idea.py
```

如果成功，會在 `ideas/` 目錄生成今天的 PRD。

#### GitHub Actions 測試

1. 前往 repo 的 **Actions** 頁面
2. 選擇 **Ingest IdeaBrowser Idea** workflow
3. 點擊 **Run workflow** > **Run workflow**
4. 查看執行結果（約 30 秒完成）

### 4. 啟用自動執行

預設每日 **UTC 13:30**（台灣時間 **21:30**）自動執行。

如需調整時間，編輯 `.github/workflows/ingest_idea.yml`：

```yaml
on:
  schedule:
    - cron: "30 13 * * *"  # 修改這裡
```

Cron 格式：`分 時 日 月 星期`（UTC 時間）

**時區換算**：
- 台灣時間 21:30 = UTC 13:30
- 台灣時間 09:00 = UTC 01:00

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
- **排程時間**: UTC 13:30（台灣時間 21:30）

### 工作流程

1. **檢查重複**: 檢查今天是否已處理過（避免浪費 API）
2. **Email Trigger**: 搜尋 IdeaBrowser 每日信件（作為觸發信號）
3. **抓取首頁**: 使用 BeautifulSoup 抓取 https://www.ideabrowser.com/ 完整內容
4. **生成 PRD**: OpenAI 閱讀完整內容後生成 PRD（包含自動分類）
5. **寫入檔案**: 儲存 PRD.md 和 meta.json
6. **Git 操作**: 自動 commit 並 push 到 GitHub

### Gmail API

- **認證方式**: OAuth 2.0 (Desktop App)
- **權限**: `gmail.readonly`
- **時區**: 台灣時區 (UTC+8)
- **搜尋條件**:
  ```python
  from:notifications@mail.ideabrowser.com
  subject:"Idea of the Day"
  after:2025/11/09
  ```

### 網頁抓取

- **工具**: BeautifulSoup + lxml
- **目標**: https://www.ideabrowser.com/
- **選擇器**: `#main-wrapper`, `#first-section`, `<article>`, `<main>`
- **清理**: 移除 script, style, nav, footer, header
- **平均長度**: 6000+ 字元

### OpenAI API

- **Model**: `gpt-4o-mini`
- **Temperature**: 0.4（保持一致性）
- **Max Tokens**: 4000
- **成本**: 約 $0.015/request，每月 < $1
- **自動分類**: 要求在 YAML frontmatter 中輸出 category 和 tags
- **語義理解**: OpenAI 閱讀完整內容後判斷，準確度遠高於關鍵字匹配

### 錯誤處理

- **重複檢查**: 流程開始就檢查，避免浪費 API 呼叫
- **OpenAI 重試**: 重試 2 次，間隔 5 秒
- **網頁抓取失敗**: 退回使用 email 摘要
- **詳細日誌**: 每個步驟都有時間戳記和狀態輸出

## 🔧 進階設定

### 自訂 PRD 格式

編輯 `scripts/ingest_idea.py` 中的 `generate_prd_with_openai()` 函式，修改 prompt：

```python
prompt = f"""你是一位資深產品經理。

請根據以下創業點子，撰寫一份完整的產品需求文件（PRD）。

**輸出格式**: Markdown with YAML Frontmatter

**必須的 YAML Frontmatter**:
---
title: [產品名稱]
category: [分類]
tags: [標籤1, 標籤2, ...]
---

**你的自訂 Markdown 章節**...
"""
```

### 分類系統

分類和標籤由 **OpenAI 自動判斷**（在生成 PRD 時一併輸出），不需要維護關鍵字列表。

**常見分類**：
- `ai`, `fintech`, `healthtech`, `edtech`, `marketplace`
- `saas`, `productivity`, `social`, `entertainment`, `hardware`
- `logistics`, `real-estate`, `travel`, `food`, `fashion`

**標籤範例**：
- `ai`, `automation`, `b2b`, `b2c`, `mobile`
- `analytics`, `marketing`, `design`, `developer-tools`

優點：
- ✅ 語義理解準確
- ✅ 自動適應新分類
- ✅ 零維護成本

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
1. `credentials.json` 是否存在且正確？
2. 是否已執行 `--auth` 並產生 `token.json`？
3. Gmail API 是否已啟用？
4. GitHub Secret `GMAIL_TOKEN_JSON` 是否正確設定（Base64 編碼）？
5. Token 是否過期？（重新執行 `--auth`）

### Q: OpenAI API 超過額度？

**A**:
1. 檢查 [OpenAI 用量頁面](https://platform.openai.com/usage)
2. 考慮使用 `gpt-3.5-turbo`（更便宜）
3. 調整 `MAX_TOKENS` 降低成本

### Q: 想要手動新增 idea？

**A**: 使用 YAML frontmatter 格式：

```bash
mkdir -p ideas/2025-11-10-my-idea
cat > ideas/2025-11-10-my-idea/PRD.md << 'EOF'
---
title: MyIdea
category: productivity
tags: [automation, mobile, mvp]
---

# 產品需求文件 (PRD)

## 產品名稱
MyIdea

...
EOF

# 產生 meta.json
echo '{
  "date": "2025-11-10",
  "title": "MyIdea",
  "source": "manual",
  "category": "productivity",
  "tags": ["automation", "mobile", "mvp"],
  "status": "new"
}' > ideas/2025-11-10-my-idea/meta.json
```

### Q: 分類不準確怎麼辦？

**A**: OpenAI 判斷的分類很準確，但如果需要調整：
1. 直接修改生成的 `PRD.md` frontmatter
2. 同步修改 `meta.json` 中的 category 和 tags
3. 或在 prompt 中加入更明確的分類指引

### Q: 能否支援其他來源（不只 IdeaBrowser）？

**A**: 可以！修改觸發和內容來源：
- **RSS feed**: 改用 feedparser 解析
- **Twitter / X**: 使用 API 抓取特定帳號
- **Notion / Obsidian**: 同步筆記資料庫
- **其他 Newsletter**: 修改 email 搜尋條件

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
