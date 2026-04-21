---
title: Salvage Marketplace
category: marketplace
tags: [trust, reclaimed materials, grading system, contractors, renovation]
---

# 產品名稱
Salvage Marketplace

# One-line Pitch
一個信任評級的回收材料市場，專為翻新承包商設計，提供標準化的材料評級系統。

# Background & Problem Statement
在翻新行業中，承包商在尋找回收材料時，常常依賴於Craigslist的帖子和回收場的實地考察，這一過程缺乏標準化的評級系統和條件驗證。由於結構完整性直接影響建築物是否能通過檢查，這樣的採購流程顯得極其不可靠。Salvage Marketplace旨在解決這一問題，通過提供標準化的評級系統，讓承包商能夠更輕鬆地找到高品質的回收材料。

# Target Users & Personas
目標用戶包括：
- **翻新承包商**：尋找高品質的回收材料以降低成本和環境影響。
- **材料供應商**：希望通過平台銷售其回收材料，並獲得更高的市場曝光度。

# User Pain Points
1. **缺乏信任**：承包商無法確定材料的真實狀況。
2. **標準化缺失**：不同供應商對材料的評級標準不一，造成選擇困難。
3. **時間浪費**：尋找合適材料的過程耗時且繁瑣。

# Value Proposition
Salvage Marketplace提供一個透明且可靠的回收材料交易平台，通過標準化的評級系統（包括結構完整性、外觀狀況和合規性評分），幫助承包商快速找到符合需求的材料，降低風險並提高工作效率。

# Core Use Cases & User Stories
1. **承包商瀏覽材料**：作為一名承包商，我希望能夠根據評級和條件快速瀏覽回收材料，以便選擇合適的材料。
2. **供應商上傳材料**：作為一名材料供應商，我希望能夠輕鬆上傳材料信息並獲得評級，以吸引潛在買家。
3. **評級系統**：作為一名用戶，我希望能夠查看材料的詳細評級信息，從而做出明智的購買決策。

# MVP Scope (Must-have vs Nice-to-have)
## Must-have
- 材料上傳功能（供應商）
- 標準化評級系統（結構完整性、外觀狀況、合規性）
- 瀏覽和搜索材料的功能
- 用戶註冊和登錄系統

## Nice-to-have
- 用戶評價系統
- 材料交易歷史記錄
- 移動端應用版本

# User Flow Overview
1. 用戶註冊/登錄
2. 供應商上傳材料信息
3. 系統自動評級或安排現場檢查
4. 承包商瀏覽材料並篩選
5. 承包商下單購買材料

# Basic System Architecture
- **前端**：React.js
- **後端**：Node.js + Express
- **數據庫**：MongoDB
- **雲存儲**：AWS S3（用於存儲材料圖片）
- **身份驗證**：JWT

# Monetization Hypothesis
- 收取供應商上傳材料的手續費
- 提供增值服務（如材料檢查、專業評估）收取費用

# Success Metrics
- 每月活躍用戶數（MAU）
- 供應商上傳的材料數量
- 平台交易總額
- 用戶滿意度評分

# Risks & Assumptions
- **風險**：市場對於標準化評級系統的接受度不高，可能影響用戶採用率。
- **假設**：承包商和供應商願意為提高交易透明度和效率而付費。