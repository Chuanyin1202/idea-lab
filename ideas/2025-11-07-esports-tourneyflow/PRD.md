# TourneyFlow - Esports Tournament Management Tool

## 產品名稱
TourneyFlow

## One-line Pitch
為電競賽事主辦方打造的一站式管理平台，自動產生對戰表、更新晉級結果，並透過 Discord / Email 自動通知選手與工作人員。

---

## Background & Problem Statement

### 現況
電競產業快速成長，但大多數社群和中小型賽事主辦方仍在使用：
* Google Sheets 手動管理對戰表
* Discord / Telegram 群組手動通知選手
* 人工更新比賽結果和晉級名單

### 問題
1. **人工作業耗時**：建立對戰表、更新結果、通知選手都需要人力
2. **容易出錯**：手動計算積分、晉級資格常出現人為錯誤
3. **選手體驗差**：等待時間長、不知道下一場對戰時間
4. **缺乏專業感**：使用 Google Sheets 降低品牌形象

---

## Target Users & Personas

### Persona 1: 社群小型賽事主辦方
* 角色：遊戲社群管理員、Discord 伺服器管理員
* 規模：10-50 人的賽事
* 痛點：沒有技術背景，需要簡單易用的工具
* 預算：有限或無預算

### Persona 2: 中型線上賽事公司
* 角色：賽事企劃、營運人員
* 規模：50-500 人的賽事
* 痛點：需要品牌化的賽事頁面，自動化流程節省人力
* 預算：願意付費使用專業工具

### Persona 3: 校園、品牌合作賽事
* 角色：學生會、品牌行銷人員
* 規模：不定，通常 20-200 人
* 痛點：需要快速建立賽事、展示贊助商資訊
* 預算：中等預算

---

## User Pain Points

1. **建立對戰表耗時**：手動分組、排程需要 1-2 小時
2. **更新結果麻煩**：每場比賽結束要更新多個地方
3. **通知選手困難**：需要逐一在 Discord 標註或發訊息
4. **缺乏即時性**：選手不知道自己何時上場
5. **數據分析困難**：賽後沒有統計報表

---

## Value Proposition

### 核心價值
**讓賽事主辦方專注在內容，而非繁瑣的行政作業**

### 關鍵優勢
1. **10 分鐘建立賽事**：填寫基本資訊，系統自動產生對戰表
2. **一鍵更新結果**：後台輸入比分，自動計算晉級名單
3. **自動通知**：Discord Bot / Email 自動通知選手下一場對戰資訊
4. **公開賽事頁**：美觀的賽事頁面，支援嵌入 Twitch 直播
5. **零技術門檻**：不需要寫程式、架伺服器

---

## Core Use Cases & User Stories

### UC1: 建立新賽事
**As a** 賽事主辦方
**I want to** 快速建立一個新賽事
**So that** 我可以開放報名並產生對戰表

**流程：**
1. 填寫賽事基本資訊（名稱、日期、遊戲類型）
2. 選擇賽制（單淘汰 / 雙淘汰 / 瑞士輪 / 分組循環）
3. 設定隊伍數量、每場比賽局數
4. 系統自動產生報名表單和對戰表
5. 分享賽事頁面給選手報名

### UC2: 管理隊伍與選手
**As a** 賽事主辦方
**I want to** 管理報名隊伍和選手資訊
**So that** 我可以確認參賽資格並安排對戰

**流程：**
1. 查看報名列表
2. 審核參賽資格（如需要）
3. 手動新增 / 移除隊伍
4. 編輯隊伍資訊（隊名、成員、Discord ID）

### UC3: 更新比賽結果
**As a** 賽事主辦方
**I want to** 快速輸入比賽結果
**So that** 系統自動更新對戰表和晉級名單

**流程：**
1. 在後台選擇比賽場次
2. 輸入雙方比分
3. 系統自動計算晉級隊伍
4. 自動通知晉級隊伍下一場對戰時間

### UC4: 自動通知選手
**As a** 選手
**I want to** 自動收到下一場對戰通知
**So that** 我不會錯過比賽時間

**流程：**
1. 主辦方更新比賽結果
2. Discord Bot 自動在指定頻道標註晉級選手
3. 或發送 Email 通知
4. 通知內容包含：對戰隊伍、時間、直播連結

### UC5: 查看公開賽事頁
**As a** 觀眾或選手
**I want to** 查看賽事對戰表和結果
**So that** 我可以追蹤賽事進度和支持的隊伍

**流程：**
1. 開啟公開賽事頁面
2. 查看對戰表、即時比分
3. 查看隊伍排名、晉級狀況
4. 觀看嵌入的 Twitch 直播（如有）

---

## MVP Scope

### Must-have (v1.0)
1. **賽事建立與設定**
   - 基本資訊設定（名稱、日期、遊戲）
   - 支援賽制：單淘汰、雙淘汰
   - 隊伍 / 選手管理

2. **自動對戰表產生**
   - 根據隊伍數量自動產生對戰表
   - 支援手動調整種子排序

3. **比賽結果更新**
   - 後台輸入比分
   - 自動更新晉級結果

4. **Discord 整合**
   - Discord Bot 通知晉級隊伍
   - 在指定頻道發布賽事更新

5. **公開賽事頁**
   - 展示對戰表和即時結果
   - RWD 響應式設計
   - 支援分享連結

### Nice-to-have (v2.0+)
1. **進階賽制**
   - 瑞士輪
   - 分組循環 + 淘汰賽
   - 自訂賽制規則

2. **Email 通知**
   - 自動發送賽程通知信
   - 比賽提醒

3. **Twitch 整合**
   - 嵌入直播畫面
   - Overlay 數據顯示

4. **贊助商管理**
   - 贊助商 Logo 展示
   - 贊助商專屬頁面

5. **賽後分析**
   - 隊伍統計數據
   - MVP 評選
   - 賽事報表下載

---

## User Flow Overview

### 主辦方流程
```
登入 → 建立賽事 → 設定賽制 → 管理報名 →
產生對戰表 → 更新比賽結果 → 自動通知選手 →
查看報表
```

### 選手流程
```
收到賽事連結 → 報名 → 收到確認通知 →
查看對戰表 → 收到比賽通知 → 參賽 →
查看結果
```

### 觀眾流程
```
開啟賽事頁 → 查看對戰表 → 追蹤支持隊伍 →
觀看直播
```

---

## Basic System Architecture

### Frontend
* **框架**：Next.js 14 (App Router)
* **UI Library**：Tailwind CSS + shadcn/ui
* **狀態管理**：Zustand
* **部署**：Vercel

### Backend
* **API**：Next.js API Routes
* **Authentication**：NextAuth.js
* **Database**：PostgreSQL (Supabase)
* **ORM**：Prisma

### Integrations
* **Discord Bot**：Discord.js
* **Email**：Resend / SendGrid
* **Storage**：Supabase Storage (隊伍 Logo 等)

### Database Schema (簡化)
```
tournaments
  - id, name, game, format, start_date, status

teams
  - id, tournament_id, name, discord_id, contact_email

matches
  - id, tournament_id, round, team1_id, team2_id,
    team1_score, team2_score, status

notifications
  - id, match_id, type, sent_at
```

---

## Monetization Hypothesis

### 定價策略

#### Freemium 模式
* **Free Tier**
  - 最多 16 隊伍
  - 單淘汰、雙淘汰賽制
  - Discord 通知
  - 有 TourneyFlow 浮水印

* **Pro Tier** ($19/month)
  - 無限隊伍
  - 所有賽制
  - Email 通知
  - 自訂品牌（移除浮水印）
  - 贊助商管理

* **Enterprise Tier** (Custom)
  - 白標服務
  - 專屬客服
  - API 存取
  - 自訂功能開發

### 收入預估
* 目標：前 6 個月獲得 100 位免費用戶
* 轉換率：10% 轉為付費用戶
* MRR：$190 (10 users × $19)
* 一年後目標：1000 用戶，10% 付費，MRR: $1,900

---

## Success Metrics

### 北極星指標
**每月活躍賽事數量（Monthly Active Tournaments）**

### 關鍵指標
1. **用戶成長**
   - 註冊用戶數
   - 建立賽事數
   - 留存率（D7, D30）

2. **產品使用**
   - 平均賽事規模（隊伍數）
   - 比賽結果更新頻率
   - 公開頁面瀏覽數

3. **變現**
   - 免費 → 付費轉換率
   - MRR 成長率
   - Churn Rate

4. **用戶滿意度**
   - NPS Score
   - 功能請求數量
   - 客服回應時間

---

## Risks & Assumptions

### Risks
1. **市場風險**
   - 現有解決方案（Battlefy, Toornament）已有市佔率
   - 小型賽事主辦方付費意願低

2. **技術風險**
   - Discord API 限制可能影響通知功能
   - 複雜賽制（瑞士輪）計算邏輯需要時間開發

3. **營運風險**
   - 需要持續客服支援
   - 用戶教學成本高

### Assumptions
1. **用戶假設**
   - 賽事主辦方願意花時間學習新工具
   - Discord 是主要溝通管道

2. **產品假設**
   - 自動化可以節省主辦方 80% 時間
   - 選手重視即時通知

3. **市場假設**
   - 電競賽事數量持續成長
   - 中小型賽事市場未被滿足

### Validation Plan
1. **訪談 10 位賽事主辦方**，確認痛點
2. **製作 Landing Page** 測試需求
3. **推出 MVP** 給 5 個種子用戶試用
4. **收集回饋** 並快速迭代
