# TourneyFlow - Esports Tournament Management Tool

為電競賽事主辦方打造的一站式管理平台，自動產生對戰表、更新晉級結果，並透過 Discord / Email 自動通知選手與工作人員。

> ✅ **MVP 已完成** - 核心功能可用，支援 4/8/16/32 隊單淘汰賽事管理
> 🚀 自動部署已啟用 - 每次推送都會自動部署到 Vercel

## 🎯 核心功能

### ✅ 已實作（MVP v1.0）
- ⚡ **快速建立賽事** - 填寫賽事資訊（名稱、遊戲、日期、隊伍數）
- 🏆 **單淘汰賽制** - 支援 4/8/16/32 隊伍，自動生成對戰表
- 👥 **隊伍管理** - 輸入所有隊伍名稱並自動排種
- 🎯 **互動式對戰表** - 視覺化顯示所有輪次（八強、準決賽、決賽）
- 📊 **即時結果更新** - 點擊對戰輸入比分，自動判定勝者並晉級
- 💾 **本地儲存** - 使用 LocalStorage 保存賽事資料

### 🚧 規劃中
- 🔔 **自動通知** - Discord Bot / Email 自動通知選手
- 🎨 **公開分享** - 生成公開連結供觀眾查看
- 🏅 **雙淘汰賽制** - 敗部復活機制

## 🚀 快速開始

### 本地開發

```bash
# 安裝依賴
npm install

# 啟動開發伺服器
npm run dev

# 開啟瀏覽器訪問 http://localhost:3000
```

### 建構生產版本

```bash
# 建構
npm run build

# 啟動生產伺服器
npm start
```

## 📱 手機測試

### 方法 1：使用 Vercel 部署版本（推薦）

專案已設定自動部署到 Vercel，每次 push 到 GitHub 後會自動部署。

- **生產環境**: 部署後會在 GitHub Actions 顯示 URL
- 直接用手機瀏覽器訪問該 URL 即可

### 方法 2：本地開發 + ngrok

```bash
# 終端 1：啟動開發伺服器
npm run dev

# 終端 2：使用 ngrok
npx ngrok http 3000

# 用手機掃描 ngrok 提供的 QR code
```

## 🔧 技術棧

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Deployment**: Vercel
- **未來整合**:
  - Database: PostgreSQL (Supabase)
  - Auth: NextAuth.js
  - Discord Bot: Discord.js

## 📂 專案結構

```
tourneyflow/
├── src/
│   └── app/
│       ├── layout.tsx       # 根 layout
│       ├── page.tsx         # 首頁
│       └── globals.css      # 全域樣式
├── public/                  # 靜態檔案
├── package.json
├── next.config.js
├── tsconfig.json
└── README.md
```

## 🚀 部署

專案已設定自動部署到 Vercel：

1. ✅ 每次 push 到 `main` 或 `claude/*` 分支
2. ✅ 修改 `projects/tourneyflow/` 目錄下的檔案
3. ✅ GitHub Actions 自動觸發部署
4. ✅ 部署完成後在 Actions 頁面查看 URL

### 手動觸發部署

前往 GitHub Actions → "Deploy Projects to Vercel" → "Run workflow"

## 📋 環境變數

複製 `.env.example` 為 `.env.local` 並填入相關資訊：

```bash
cp .env.example .env.local
```

目前專案尚未需要環境變數，未來整合 Supabase 和 Discord 時會需要。

## 📖 開發計畫

### Phase 1: Landing Page（目前階段）
- [x] 基礎 Next.js 專案架構
- [x] 首頁設計
- [x] Vercel 自動部署
- [ ] RWD 響應式優化

### Phase 2: MVP 核心功能
- [ ] 賽事建立功能
- [ ] 對戰表自動生成（單/雙淘汰）
- [ ] 比賽結果更新
- [ ] Discord Bot 通知

### Phase 3: 進階功能
- [ ] 用戶認證系統
- [ ] 隊伍管理
- [ ] Twitch 直播整合
- [ ] 賽後統計

## 📄 授權

此專案為 Idea Lab 的一部分，詳見 [idea-lab](https://github.com/Chuanyin1202/idea-lab)

## 🔗 相關連結

- [PRD 文件](../../ideas/2025-11-07-esports-tourneyflow/PRD.md)
- [專案架構](../../ARCHITECTURE.md)
