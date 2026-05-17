---
title: Transom
category: saas
tags: [real-estate, automation, crm, productivity, workflow]
---

# 產品名稱
Transom

# One-line Pitch
一個集成的房地產工作流程自動化平台，將多個工具整合為一個無縫的工作體驗。

# Background & Problem Statement
目前的房地產經紀人需要使用多個獨立的軟體工具來管理客戶關係、文件處理和市場推廣。然而，這些工具之間缺乏整合，導致經紀人需要重複輸入相同的客戶資訊，增加了工作負擔和錯誤的可能性。這不僅延遲了回應時間，還可能導致交易的損失。

# Target Users & Personas
- **房地產經紀人**：需要有效管理客戶資料、跟進潛在客戶並處理交易文件。
- **房地產經紀公司**：希望提高團隊效率，減少重複性工作，並提升客戶滿意度。
- **市場推廣專員**：需要整合不同平台的數據以提高行銷活動的效果。

# User Pain Points
1. 重複輸入客戶資料到多個系統。
2. 各平台之間缺乏數據共享，導致信息孤島。
3. 手動處理的流程繁瑣，容易出錯。
4. 回應潛在客戶的速度慢，影響業務機會。

# Value Proposition
Transom 提供一個集成平台，將 Zillow、Follow Up Boss、Dotloop 和電子郵件系統整合，實現自動化工作流程，減少手動輸入，提高工作效率，並加快客戶回應時間。

# Core Use Cases & User Stories
1. **自動化客戶資料輸入**：當潛在客戶從 Zillow 進入系統時，自動創建 CRM 聯絡人並啟動跟進流程。
   - *用戶故事*：作為一名房地產經紀人，我希望能夠自動將潛在客戶資料導入 CRM，以便快速跟進。
   
2. **文件管理自動化**：自動生成和管理交易所需的文件，並將其存儲在 Dotloop 中。
   - *用戶故事*：作為一名經紀人，我希望能夠自動生成文件，減少手動處理的時間。

3. **行銷活動自動化**：根據客戶行為自動啟動行銷活動。
   - *用戶故事*：作為市場推廣專員，我希望能夠根據客戶的互動自動發送行銷郵件。

# MVP Scope
## Must-have
- 整合 Zillow、Follow Up Boss 和 Dotloop。
- 自動創建 CRM 聯絡人。
- 自動生成交易文件。
- 基本的行銷活動自動化功能。

## Nice-to-have
- 數據分析儀表板，提供業務洞察。
- 高級行銷活動管理功能。
- 多語言支持。

# User Flow Overview
1. 潛在客戶從 Zillow 進入系統。
2. 系統自動創建 CRM 聯絡人。
3. 觸發行銷活動的自動化流程。
4. 生成並存儲所需的交易文件。

# Basic System Architecture
- **前端**：React.js
- **後端**：Node.js + Express
- **數據庫**：MongoDB
- **第三方 API**：Zillow API, Follow Up Boss API, Dotloop API
- **雲服務**：AWS 或 Google Cloud

# Monetization Hypothesis
- 訂閱制收費模型，根據用戶數量和功能模塊收取月費或年費。
- 提供增值服務，如數據分析和高級行銷功能。

# Success Metrics
- 用戶滿意度調查結果。
- 每月活躍用戶數 (MAU)。
- 客戶轉換率（從潛在客戶到付費用戶）。
- 減少手動輸入的時間。

# Risks & Assumptions
- 風險：市場接受度不高，競爭對手的壓力。
- 假設：用戶願意為自動化解決方案支付額外費用，並且對整合工具有需求。