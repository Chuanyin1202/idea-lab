# OAuth 2.0 設定指南

## 📋 完成設定步驟

✅ 你已完成以下步驟：
1. ✅ 建立 Google Cloud Project
2. ✅ 啟用 Gmail API
3. ✅ 建立 OAuth 2.0 憑證（電腦版應用程式）
4. ✅ 下載並複製 `credentials.json`
5. ✅ 本機執行授權並產生 `token.json`

---

## 🔐 設定 GitHub Secrets

現在需要設定 2 個 GitHub Secrets：

### 1. `OPENAI_API_KEY`

前往 https://github.com/Chuanyin1202/idea-lab/settings/secrets/actions

- **Name**: `OPENAI_API_KEY`
- **Secret**: 你的 OpenAI API key（**請先撤銷之前外洩的 key！**）

⚠️ **重要**：你之前不小心貼出的 API key 已經外洩，請立即：
1. 前往 https://platform.openai.com/api-keys
2. 撤銷該 key
3. 建立新的 API key
4. 將新 key 貼到 GitHub Secret

---

### 2. `GMAIL_TOKEN_JSON`

**Base64 編碼的 token 已經產生**：

```
eyJ0b2tlbiI6ICJ5YTI5LmEwQVRpNksydkN5akxMU3N0WTJhWG1tZzA5dDhFUW1ESjlWWFdGSS1GQXd2OEc3NnZmUlhNSWkzX3U0RExhanVMaXl6TDRPNy1jTHRVdGxWUkxqWjdKYThYY1BrbUViQmRKWmZVT09GNFRKOW9vT190dUxCaEZFRk1TNGE2SHdKZUNUTms1ZUw3ejR5cTlmSjlOd0l0dmdjSGk4VkY0OTFxTGhCWWlVSlF0eUw0Rk9DOE10VEhiTUx1YjNIRnNqM2JSNFdsZS1Fb2FDZ1lLQVFvU0FSRVNGUUhHWDJNaXRldHJYZTgwSldWaEMzVk1rZnFUd1EwMjA2IiwgInJlZnJlc2hfdG9rZW4iOiAiMS8vMGZORTNRZnlmTEgzbUNnWUlBUkFBR0E4U053Ri1MOUlyWlFKZGE0R3AyTDNZbEFXalR5cVJFVHEzdmRPanNieklOQ1I4QWtwLXpZZ0tLQ3FPang4YllLbDY4TDlnTjlhYi05cyIsICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLCAiY2xpZW50X2lkIjogIjkyNTQ2MDU1MzU2OC1sNjRsZHZxc25qa3R1cXBzbzkyN203OGw4MzgwOWRjai5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsICJjbGllbnRfc2VjcmV0IjogIkdPQ1NQWC1EWnowNXJCNXRLMjB2YkEwal9ocG1WQ1FZRVozIiwgInNjb3BlcyI6IFsiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vYXV0aC9nbWFpbC5yZWFkb25seSJdLCAidW5pdmVyc2VfZG9tYWluIjogImdvb2dsZWFwaXMuY29tIiwgImFjY291bnQiOiAiIiwgImV4cGlyeSI6ICIyMDI1LTExLTA3VDE4OjA3OjM1WiJ9
```

**設定步驟**：
1. 前往 https://github.com/Chuanyin1202/idea-lab/settings/secrets/actions
2. 點擊 **New repository secret**
3. **Name**: `GMAIL_TOKEN_JSON`
4. **Secret**: 貼上上面的 Base64 編碼內容
5. 點擊 **Add secret**

---

## 🧪 測試 GitHub Actions

設定完 secrets 後：

1. 前往 https://github.com/Chuanyin1202/idea-lab/actions
2. 選擇 **Ingest IdeaBrowser Idea** workflow
3. 點擊 **Run workflow**
4. 查看執行結果

**預期結果**：
- 如果今天有收到 IdeaBrowser 信件 → 成功建立 PRD
- 如果今天沒收到信 → 顯示「找不到符合條件的信件」（正常）

---

## ⚠️ Token 過期處理

Gmail OAuth token 會過期，屆時需要重新授權：

### 症狀
- GitHub Actions 失敗，錯誤訊息：`Token 更新失敗`
- 或：`❌ OAuth 授權失敗`

### 解決方式

#### 方案 1：本機重新授權（推薦）

```bash
cd /Users/alexhuang/Development/idea-lab
source venv/bin/activate
export OPENAI_API_KEY="your-key"
python scripts/ingest_idea.py --reauth
```

然後產生新的 Base64 token：

```bash
base64 -i token.json | pbcopy
```

更新 GitHub Secret `GMAIL_TOKEN_JSON`

#### 方案 2：刪除 token 重新授權

```bash
rm token.json
python scripts/ingest_idea.py --auth
```

---

## 📝 待辦事項（收到 IdeaBrowser 信件後）

收到第一封 IdeaBrowser 信件時，需要調整搜尋條件：

1. 查看信件的實際寄件者和主旨
2. 編輯 `scripts/ingest_idea.py` 第 36-37 行：

```python
IDEABROWSER_FROM = '實際寄件者@email.com'
IDEABROWSER_SUBJECT = '實際主旨'
```

3. 提交並推送更新：

```bash
git add scripts/ingest_idea.py
git commit -m "fix: update IdeaBrowser email search criteria"
git push
```

---

## ✅ 設定完成檢查清單

- [ ] 撤銷外洩的 OpenAI API key
- [ ] 建立新的 OpenAI API key
- [ ] 設定 GitHub Secret: `OPENAI_API_KEY`
- [ ] 設定 GitHub Secret: `GMAIL_TOKEN_JSON`
- [ ] 測試 GitHub Actions workflow
- [ ] 等待收到第一封 IdeaBrowser 信件
- [ ] 調整信件搜尋條件（收到信後）

---

**需要幫助？**

如果遇到問題，檢查：
1. GitHub Secrets 是否正確設定
2. Token 是否過期（重新授權）
3. Gmail API 權限是否足夠
4. OpenAI API key 是否有效

祝順利！🎉
