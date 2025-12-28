---
title: Rebate Hunter
category: saas
tags: [rebates, energy efficiency, homeowners, contractors, automation]
---

# 產品名稱
Rebate Hunter

# One-line Pitch
透過 Rebate Hunter，讓家庭輕鬆獲得綠色家居改造的回饋金，最大化節能改造的經濟效益。

# Background & Problem Statement
隨著政府推動家庭電氣化，許多家庭在進行節能改造（如安裝熱泵、太陽能電池板等）時，往往錯過了可申請的回饋金。根據《通脹減少法案》，美國政府提供了數十億美元的回饋金和稅收抵免，但由於資訊分散且複雜，許多家庭未能成功申請這些資源。Rebate Hunter 將幫助用戶導航這些繁瑣的程序，確保他們能夠獲得應有的回饋金。

# Target Users & Personas
- **家庭用戶**：希望進行家居改造並獲得回饋金的房主，對節能和環保有興趣。
- **承包商**：需要為客戶提供回饋金資訊的專業人士，經常進行多次查詢以展示實際價格。

# User Pain Points
- 資訊分散：回饋金的資訊來自不同的聯邦、州和公用事業機構，導致用戶難以獲得全面的資訊。
- 繁瑣的申請流程：用戶對申請流程不熟悉，容易錯過截止日期或要求。
- 缺乏透明度：用戶不清楚自己能夠申請哪些回饋金及其金額。

# Value Proposition
Rebate Hunter 提供一個簡單易用的網頁應用，讓用戶只需輸入項目和郵遞區號，即可快速獲得所有符合資格的回饋金資訊，並提供詳細的申請步驟，幫助用戶最大化其節能改造的經濟效益。

# Core Use Cases & User Stories
1. **家庭用戶查詢**：
   - 角色：家庭用戶
   - 故事：作為一名家庭用戶，我希望能夠輸入我的家居改造項目和郵遞區號，以便快速獲得所有可申請的回饋金資訊。
   
2. **承包商查詢**：
   - 角色：承包商
   - 故事：作為一名承包商，我希望能夠為我的客戶進行多次查詢，以便展示改造後的實際價格及可獲得的回饋金。

# MVP Scope (Must-have vs Nice-to-have)
## Must-have
- 用戶輸入項目和郵遞區號的功能
- 自動生成符合資格的回饋金列表
- 詳細的申請步驟指導
- 數據庫的建立與更新（爬蟲技術）

## Nice-to-have
- 用戶評價系統，分享申請經驗
- 整合社交媒體分享功能
- 多語言支持

# User Flow Overview
1. 用戶訪問 Rebate Hunter 網站
2. 用戶輸入家居改造項目和郵遞區號
3. 系統檢索數據庫，顯示所有可申請的回饋金
4. 用戶查看詳細的申請步驟
5. 用戶根據指導完成申請

# Basic System Architecture
- **前端**：React.js
- **後端**：Node.js + Express
- **數據庫**：MongoDB
- **爬蟲技術**：使用 Python 的 BeautifulSoup 和 Scrapy 進行數據抓取
- **雲服務**：AWS 或 Google Cloud 用於部署和數據存儲

# Monetization Hypothesis
- 每份報告收費 $29，針對家庭用戶。
- 每月收費 $299，針對需要多次查詢的承包商。

# Success Metrics
- 每月活躍用戶數（MAU）
- 每月報告銷售數量
- 用戶滿意度評分
- 申請成功率

# Risks & Assumptions
- **風險**：數據來源的變更可能影響系統的準確性；市場競爭可能導致用戶流失。
- **假設**：用戶願意為簡化的申請流程支付費用；承包商會主動尋找此類工具以提高服務質量。