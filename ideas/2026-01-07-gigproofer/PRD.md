---
title: GigProofer
category: fintech
tags: [income verification, gig economy, mobile, b2c, automation]
---

# 產品名稱
GigProofer

# One-line Pitch
為零工工作者提供收入驗證的應用程式，幫助他們獲得貸款。

# Background & Problem Statement
隨著零工經濟的興起，越來越多的人依賴平台如Uber、Lyft、DoorDash等來賺取收入。然而，傳統銀行系統仍然主要依賴W-2表格來驗證收入，這使得許多零工工作者在申請貸款時面臨困難。即使他們的收入穩定且已繳稅，銀行卻不承認他們的1099收入，導致他們被迫接受高利貸的貸款條件。GigProofer旨在填補這一缺口，提供一個簡單的解決方案來驗證零工工作者的收入。

# Target Users & Personas
- **主要使用者**: 零工工作者（如Uber司機、DoorDash送餐員）
- **次要使用者**: 銀行及貸款機構的貸款官
- **Persona**: 
  - **Alice**: 32歲的DoorDash司機，年收入$62,000，因無法提供正確的收入證明而被拒貸。
  - **Bob**: 銀行貸款官，經常面對零工工作者的貸款申請，對其收入來源感到困惑。

# User Pain Points
1. 零工工作者無法提供傳統的收入證明（如W-2或工資單）。
2. 銀行對零工收入的認知不足，導致貸款申請被拒。
3. 高利貸貸款選擇限制了零工工作者的財務自由。

# Value Proposition
GigProofer提供一個自動化的平台，能夠從多個零工平台提取真實的收入數據，並生成可供貸款機構使用的收入驗證文件。這不僅幫助零工工作者獲得貸款，還提高了銀行對零工收入的認識。

# Core Use Cases & User Stories
1. **使用者故事**: 
   - 作為一名零工工作者，我希望能夠輕鬆獲取我的收入報告，以便在申請貸款時提供給銀行。
   - 作為一名貸款官，我希望能夠快速驗證零工工作者的收入，以便做出更快的貸款決策。

# MVP Scope (Must-have vs Nice-to-have)
- **Must-have**:
  - 整合主要零工平台（Uber, Lyft, DoorDash, Instacart）。
  - 自動生成收入驗證PDF報告。
  - 用戶註冊和登錄系統。
  
- **Nice-to-have**:
  - 提供收入趨勢分析和預測功能。
  - 整合多種貸款機構的申請流程。

# User Flow Overview
1. 使用者註冊並連接其零工平台帳戶。
2. 系統提取收入數據並生成報告。
3. 使用者下載報告並提交給貸款機構。
4. 銀行接收報告並進行貸款審核。

# Basic System Architecture
- **前端**: React Native (移動應用)
- **後端**: Node.js + Express (API服務)
- **數據庫**: MongoDB (用於存儲用戶數據和報告)
- **第三方API**: 各零工平台的API（如Uber, DoorDash等）

# Monetization Hypothesis
- 每月收取$9.99的訂閱費用。
- 每筆成功貸款從貸款機構收取$25-$50的手續費。

# Success Metrics
1. 每月活躍用戶數 (MAU)
2. 每月生成的收入報告數量
3. 成功獲得貸款的用戶比例

# Risks & Assumptions
- **風險**: 零工平台可能會限制數據訪問，影響收入提取的準確性。
- **假設**: 銀行願意接受GigProofer生成的報告作為收入驗證的依據。