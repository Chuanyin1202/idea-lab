# idea-lab 架構說明

## 核心目的

這個 Repo 是一個「個人 Idea / MVP 孵化實驗室」。

自動流程每天會：

1. 從 IdeaBrowser 的每日信件透過 Gmail API 取得當日創業點子
2. 用 OpenAI gpt-4o-mini 轉換成標準化的 `PRD.md`
3. 存進 `ideas/` 資料夾，並更新 `SUMMARY.md`
4. 不自動建立新 repo、不自動動到實作專案，只在這個 monorepo 裡管理資料

當某個 idea 值得實作時，再在 `projects/` 下建立對應專案，由人類 + AI 一起開發。

---

## 目錄結構

```bash
idea-lab/
  ideas/
    YYYY-MM-DD-slug/
      PRD.md      # 由 LLM 產生的完整產品需求文件
      meta.json   # 該 idea 的結構化資訊
  projects/
    {project-name}/
      ...         # 實作中的 MVP 專案 (Next.js / API / etc.)
  scripts/
    ingest_idea.py  # 由 GitHub Actions 呼叫，負責抓取 Idea 並寫入 ideas/
  SUMMARY.md        # 所有 ideas 的索引表（自動維護）
  .github/
    workflows/
      ingest_idea.yml  # 每日自動執行 ingest_idea.py 的排程設定
```

---

## 命名與規則

### ideas/

* 每個 idea 一個資料夾：
  * `ideas/{YYYY-MM-DD}-{slug-title}/`
  * 例如：`ideas/2025-11-07-esports-tourneyflow/`
* 必含檔案：
  * `PRD.md`：完整 PRD
  * `meta.json`：統一格式，至少：

```json
{
  "date": "2025-11-07",
  "title": "TourneyFlow - Esports tournament management tool",
  "source": "ideabrowser",
  "category": "esports",
  "tags": ["mvp", "saas", "automation", "discord"],
  "status": "new"
}
```

### SUMMARY.md

* 作為簡易索引表
* 新增 idea 後會在表格中加一行
* 方便人類 / AI 快速瀏覽與篩選

格式範例：

```markdown
# Idea Summary

| Date       | Title                                                | Category | Tags                          |
|------------|------------------------------------------------------|----------|-------------------------------|
| 2025-11-07 | [TourneyFlow - Esports Tool](ideas/2025-11-07-esports-tourneyflow/PRD.md) | esports  | mvp, saas, automation, discord |
```

---

## 自動化流程規格

由 `.github/workflows/ingest_idea.yml` 定時觸發：

1. `actions/checkout` 把 repo 拉下來
2. 執行 `scripts/ingest_idea.py`
3. 若有新檔案產生：
   * 自動 `git commit` ＋ `git push`
4. 若無新 idea 或已存在：
   * 不做變更

### 限制條件（重要）

* 自動化**只能修改**：
  * `ideas/**`
  * `SUMMARY.md`
* 不得自動修改：
  * `projects/**`
* 若當日目錄已存在則跳過（避免重複生成）

---

## 從 Idea 到 Project 的操作流程

1. 人類打開 `SUMMARY.md`，挑選有興趣的 idea。
2. 查看該 idea 的 `PRD.md`。
3. 決定要實作 → 在 `projects/` 建立專案資料夾，例如：

```bash
projects/tourneyflow/
  web/
  README.md
```

4. 在 `projects/tourneyflow/README.md` 中標註來源：

```markdown
# TourneyFlow

Source Idea: [2025-11-07-esports-tourneyflow](../../ideas/2025-11-07-esports-tourneyflow/PRD.md)
```

5. 接著可以請 AI（例如 Claude Code）根據 PRD：
   * 建立 Next.js / React 專案骨架
   * 實作 API / DB schema / 前端頁面

---

## CI/CD 建議

* 自動 ingest 工作流：`ingest_idea.yml`
  * 只處理 ideas & SUMMARY，不觸發部署

* 各專案 deployment workflow：
  * 放在 `.github/workflows/`，命名依專案命名
  * `on.push.paths` 限制到專案目錄，例如：

```yaml
on:
  push:
    paths:
      - "projects/tourneyflow/**"
      - ".github/workflows/tourneyflow-deploy.yml"
```

這樣每日自動寫入 PRD 不會誤觸所有部署流程。

---

## 給 AI（Claude Code / ChatGPT 等）的使用說明

當 AI 在這個 repo 中工作時，遵守以下原則：

1. 若任務是「新增每日 Idea」：
   * 只允許修改：
     * `ideas/**`
     * `SUMMARY.md`

2. 若任務是「建立某個 MVP 實作」：
   * 先確認對應 `ideas/.../PRD.md`
   * 在 `projects/{project-name}/` 建立結構與程式碼

3. 不要自動刪除既有 idea 資料夾與 meta.json

4. 不要自動改寫 PRD，除非使用者明確要求「更新這個 PRD」

此架構目標：
讓人類可以用手機 + 雲端 IDE / Claude Code，在**同一 repo 中**完成：

* 自動收集想法
* 閱讀 PRD
* 啟動實作

而不需要手動建立多個新 repo。

---

## 技術架構

### Gmail API 整合

使用 Gmail API 透過 Service Account 自動抓取 IdeaBrowser 每日信件：

* 認證方式：OAuth 2.0 with Service Account
* 搜尋條件：
  * `from:ideas@ideabrowser.com`
  * `subject:"Idea of the Day"`
  * `after:{yesterday}`

### LLM PRD 生成

使用 OpenAI gpt-4o-mini：

* 成本：~$0.015/1M tokens input, ~$0.06/1M tokens output
* 每月約 30 次呼叫，成本 < $1
* 溫度參數：0.4（保持一致性）

### 錯誤處理

* Gmail API 失敗：重試 3 次，間隔 5 秒
* OpenAI API 失敗：重試 2 次
* 所有失敗發送 GitHub Actions 錯誤通知
