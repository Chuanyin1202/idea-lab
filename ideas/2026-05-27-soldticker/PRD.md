---
title: Soldticker
category: marketplace
tags: [pricing, analytics, chrome-extension, e-commerce]
---

# 產品名稱
Soldticker

# One-line Pitch
一款為TikTok Shop賣家提供實時銷售價格數據的Chrome擴展，幫助他們做出更明智的定價決策。

# Background & Problem Statement
目前，TikTok Shop的賣家面臨著定價不透明的問題。雖然他們可以查看競爭對手的標價，但卻無法獲得實際銷售數據，這導致他們在定價時經常猜測，從而影響了銷售轉化率和利潤。相比之下，Amazon和Shopify的賣家擁有強大的定價分析工具，這使得TikTok Shop的賣家在市場競爭中處於劣勢。

# Target Users & Personas
- **賣家Persona**: TikTok Shop賣家，通常是小型企業主或個人創業者，對市場數據的需求高，但缺乏資源進行深入分析。
- **年齡範圍**: 20-40歲
- **技術能力**: 中等，熟悉基本的網絡應用和工具。

# User Pain Points
1. 缺乏實時銷售數據，導致定價不準確。
2. 無法評估競爭對手的實際銷售表現。
3. 定價過高或過低均影響銷售業績。
4. 無法快速獲取市場趨勢和需求變化的反饋。

# Value Proposition
Soldticker通過提供TikTok Shop、Amazon和Shopify的實際銷售數據，幫助賣家做出更準確的定價決策，從而提升銷售轉化率和利潤，減少猜測帶來的風險。

# Core Use Cases & User Stories
1. **用例1**: 賣家在TikTok Shop上瀏覽產品，使用Soldticker擴展查看相似產品的過去30天銷售數據。
   - **用戶故事**: 作為一名賣家，我希望能快速查看競爭對手的銷售價格，以便我能夠設定合理的價格。
   
2. **用例2**: 賣家根據Soldticker提供的數據調整自己的產品價格。
   - **用戶故事**: 作為一名賣家，我希望根據實際銷售數據來調整我的產品價格，以提高我的銷售量。

# MVP Scope (Must-have vs Nice-to-have)
## Must-have
- 提供TikTok Shop、Amazon和Shopify的實際銷售數據。
- Chrome擴展的基本功能，包括數據查詢和顯示。
- 用戶友好的界面設計。

## Nice-to-have
- 數據可視化功能，例如圖表和趨勢分析。
- 自定義報告功能，讓用戶能夠下載數據。
- 通知功能，當競爭對手價格變動時提醒用戶。

# User Flow Overview
1. 用戶安裝Soldticker Chrome擴展。
2. 用戶在TikTok Shop上瀏覽產品。
3. 用戶點擊Soldticker擴展圖標。
4. 擴展顯示相似產品的實際銷售數據。
5. 用戶根據數據調整自己的產品價格。

# Basic System Architecture
- **前端**: 使用React框架開發Chrome擴展。
- **後端**: Node.js和Express作為API服務器。
- **數據庫**: MongoDB用於存儲銷售數據。
- **數據來源**: 通過API抓取TikTok Shop、Amazon和Shopify的銷售數據。

# Monetization Hypothesis
Soldticker可以採用訂閱制收費模式，提供免費試用期，之後根據用戶的需求和功能進行分級收費。

# Success Metrics
1. 每月活躍用戶數(MAU)。
2. 用戶留存率。
3. 用戶滿意度調查結果。
4. 用戶通過Soldticker調整價格後的銷售增長百分比。

# Risks & Assumptions
- **風險**: 數據抓取的合法性和穩定性可能影響產品的可行性。
- **假設**: 用戶對於實時銷售數據的需求足夠高，願意為此付費。