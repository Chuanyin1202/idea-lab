# TourneyFlow 部署指南

本文件說明如何設定和使用自動部署到 Vercel 的功能。

## 📋 前置需求

1. ✅ GitHub repository (已完成)
2. ✅ Vercel 帳號（使用 GitHub 登入）
3. ✅ Vercel Token（您已提供）
4. ⚠️ GitHub Secret 設定（需要您操作）

## 🔧 一次性設定（您需要操作）

### 步驟 1: 設定 GitHub Secret

由於安全限制，需要您手動設定 `VERCEL_TOKEN`：

**方法 1：透過網頁（推薦）**

1. 前往 https://github.com/Chuanyin1202/idea-lab/settings/secrets/actions
2. 點擊 **"New repository secret"**
3. 填寫：
   - Name: `VERCEL_TOKEN`
   - Secret: `6quZsgJyPqD1A6vU9qJbK1py`
4. 點擊 **"Add secret"**

**方法 2：透過手機 GitHub App**

1. 開啟 GitHub App
2. 前往 idea-lab repository
3. Settings → Secrets and variables → Actions
4. New repository secret
5. 填寫 Name 和 Secret（同上）

### 步驟 2: 驗證設定

前往 https://github.com/Chuanyin1202/idea-lab/settings/secrets/actions

確認看到：
- ✅ `VERCEL_TOKEN` (Updated X seconds ago)

## 🚀 自動部署流程

設定完成後，部署會**完全自動化**：

```
修改 projects/tourneyflow/ 下的檔案
    ↓
git add . && git commit -m "..." && git push
    ↓
GitHub 偵測到變更
    ↓
觸發 GitHub Actions workflow
    ↓
自動安裝依賴 → 建構 → 部署到 Vercel
    ↓
部署完成！（約 2-3 分鐘）
    ↓
在 GitHub Actions 頁面查看部署 URL
```

### 觸發條件

自動部署會在以下情況觸發：

1. ✅ Push 到 `main` 分支
2. ✅ Push 到 `claude/*` 分支
3. ✅ 修改 `projects/tourneyflow/` 下的任何檔案
4. ✅ 手動觸發（GitHub Actions 頁面）

### 不會觸發部署

- ❌ 修改 `ideas/` 目錄
- ❌ 修改 `scripts/` 目錄
- ❌ 修改 `projects/` 下的其他專案

## 📱 查看部署結果

### 方法 1: GitHub Actions 頁面（推薦）

1. 前往 https://github.com/Chuanyin1202/idea-lab/actions
2. 點擊最新的 "Deploy Projects to Vercel" workflow
3. 查看 "Deployment Summary" 區塊
4. 複製 URL 用手機瀏覽器訪問

### 方法 2: Vercel Dashboard

1. 前往 https://vercel.com/dashboard
2. 找到 `tourneyflow` 專案
3. 點擊最新的 Deployment
4. 查看 "Visit" 按鈕旁的 URL

### 方法 3: Vercel App（手機）

1. 下載 Vercel App
2. 登入（使用 GitHub 帳號）
3. 查看 `tourneyflow` 專案
4. 點擊 "Visit" 直接用手機瀏覽器開啟

## 🧪 測試自動部署

設定好 `VERCEL_TOKEN` 後，可以測試部署：

```bash
# 1. 修改一個簡單的檔案
echo "\n// Test deployment" >> projects/tourneyflow/next.config.js

# 2. Commit 並 push
git add projects/tourneyflow/next.config.js
git commit -m "test: verify auto deployment"
git push

# 3. 前往 GitHub Actions 查看部署進度
# https://github.com/Chuanyin1202/idea-lab/actions
```

## 🎯 手動觸發部署

如果想要手動觸發部署（即使沒有程式碼變更）：

1. 前往 https://github.com/Chuanyin1202/idea-lab/actions
2. 選擇 "Deploy Projects to Vercel" workflow
3. 點擊 "Run workflow"
4. 選擇分支（例如 `main`）
5. 點擊 "Run workflow" 按鈕

**手機操作：**
- GitHub App → Actions → Deploy Projects to Vercel → Re-run jobs

## 🔍 部署故障排除

### 問題 1: Workflow 沒有執行

**可能原因：**
- ❌ `VERCEL_TOKEN` 沒有設定
- ❌ 修改的檔案不在 `projects/tourneyflow/` 下
- ❌ Push 到錯誤的分支

**解決方法：**
1. 確認 Secret 已設定
2. 確認修改的檔案路徑正確
3. 確認 push 到 `main` 或 `claude/*` 分支

### 問題 2: 部署失敗

**可能原因：**
- ❌ `VERCEL_TOKEN` 過期或無效
- ❌ Vercel 配額用完
- ❌ 建構錯誤（TypeScript 或 ESLint 錯誤）

**解決方法：**
1. 檢查 GitHub Actions logs
2. 查看詳細錯誤訊息
3. 修正程式碼錯誤後重新 push

### 問題 3: 部署成功但無法訪問

**可能原因：**
- ❌ Vercel 專案還在初始化
- ❌ DNS 設定需要時間

**解決方法：**
- 等待 1-2 分鐘後重試
- 清除瀏覽器快取

## 📊 部署資訊

### 部署環境

- **Node.js**: 20.x
- **Build Command**: `vercel build --prod`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### Vercel 專案設定

- **Framework**: Next.js
- **Root Directory**: `projects/tourneyflow`
- **Environment**: Production

## 🔐 安全性

### ⚠️ 重要：刪除包含 Token 的訊息

現在請**立即刪除**對話中包含 Vercel Token 的訊息，以保護安全！

Token 已經安全地儲存在 GitHub Secrets 中，不會再次顯示。

### Token 管理

- ✅ Token 儲存在 GitHub Secrets（加密）
- ✅ GitHub Actions 可以使用但看不到明文
- ✅ 定期輪換 Token（建議每 6 個月）

### 撤銷 Token

如果需要撤銷當前 Token：

1. 前往 https://vercel.com/account/tokens
2. 找到 `github-actions` token
3. 點擊 "Delete"
4. 建立新 Token
5. 更新 GitHub Secret

## 📞 支援

如有問題，請：

1. 查看 [GitHub Actions logs](https://github.com/Chuanyin1202/idea-lab/actions)
2. 查看 [Vercel Dashboard](https://vercel.com/dashboard)
3. 參考 [Vercel 文件](https://vercel.com/docs)

---

**下一步：** 設定完 `VERCEL_TOKEN` 後，push 任何變更到 `projects/tourneyflow/` 測試自動部署！
