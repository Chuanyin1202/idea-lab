---
title: Tenpay
category: fintech
tags: [accounting, automation, b2b, saas, creator-economy]
---

# 產品名稱
Tenpay

# One-line Pitch
一個專為內容創作者設計的連接平台會計工具，簡化收入分類和稅務計算，讓創作者專注於創作。

# Background & Problem Statement
隨著創作者經濟的快速發展，許多中型創作者的收入來源變得多樣化，包括廣告收入、訂閱、數位產品、贊助和聯盟計畫。傳統的會計工具如QuickBooks無法滿足這些創作者的需求，因為它們設計時假設企業有單一的收入來源和可預測的支出。這導致許多創作者需要花費大量時間進行會計工作，並且會計師在處理這些複雜的收入來源時也面臨挑戰。因此，我們需要一個能夠自動化這些流程的工具，以減少時間和人力成本。

# Target Users & Personas
1. **內容創作者**：例如YouTuber、Podcaster、Instagram影響者，通常需要管理多個收入來源。
2. **會計師**：專門為創作者提供服務的會計師，幫助他們處理複雜的財務狀況。

# User Pain Points
- 需要花費數小時進行收入分類和稅務計算。
- 不同平台的收入結構和費用分配不一致，增加了會計的複雜性。
- 會計師需要不斷追蹤和修正錯誤，浪費時間和資源。

# Value Proposition
Tenpay通過自動化收入分類和稅務計算，幫助創作者和會計師節省時間，提升效率，讓他們能夠專注於創作和客戶服務。它能夠實時更新稅務義務，並學習每筆交易的分類規則，減少人工干預。

# Core Use Cases & User Stories
1. **創作者使用案例**：
   - 作為一名YouTuber，我希望能夠自動導入我的廣告收入和贊助收入，這樣我就不需要手動輸入數據。
  
2. **會計師使用案例**：
   - 作為一名會計師，我希望能夠查看所有客戶的收入報告，這樣我就可以快速識別問題並提供建議。

# MVP Scope (Must-have vs Nice-to-have)
## Must-have
- Stripe集成以導入交易數據。
- 自動收入分類和稅務計算功能。
- 基本的報告功能。

## Nice-to-have
- 支持多平台的API集成。
- 高級報告和分析功能。
- 用戶自定義的分類規則。

# User Flow Overview
1. 用戶註冊並連接Stripe帳戶。
2. 系統自動導入交易數據。
3. 系統根據過去的數據自動分類收入。
4. 用戶查看報告和稅務義務。
5. 用戶可進行手動調整和自定義分類。

# Basic System Architecture
- **前端**：React.js
- **後端**：Node.js + Express
- **數據庫**：MongoDB
- **第三方API**：Stripe API
- **雲服務**：AWS或Google Cloud

# Monetization Hypothesis
我們將以每月49美元的價格為個人創作者提供服務，並以199美元的價格為管理多個客戶的會計師提供服務。預期通過提供高效的會計解決方案，能夠吸引大量用戶並實現穩定的收入。

# Success Metrics
- 每月活躍用戶數（MAU）。
- 用戶留存率。
- 每位用戶的平均收入（ARPU）。
- 收入分類和稅務計算的時間減少50%。

# Risks & Assumptions
- 用戶對自動化分類的信任度可能較低，需要時間來建立信任。
- 第三方API的變更可能影響系統的穩定性。
- 市場需求的變化可能影響用戶的付費意願。