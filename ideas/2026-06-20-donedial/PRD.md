---
title: Donedial
category: healthtech
tags: [ai, automation, b2b, voice-assistant]
---

# 產品名稱
Donedial

# One-line Pitch
一個智能語音助手，幫助小型醫療和牙科診所自動處理保險查詢，節省時間並降低拒絕索賠的風險。

# Background & Problem Statement
在小型醫療和牙科診所中，前台人員需要花費大量時間撥打保險公司電話，等待接通並導航自動菜單，這一過程通常需要每週花費10小時。每一次漏掉的查詢可能導致高達2000美元的索賠被拒。因此，開發一個能夠自動化這一過程的解決方案是非常必要的。

# Target Users & Personas
- **前台人員**：負責處理病人登記和保險查詢的工作，通常工作繁忙且壓力大。
- **診所管理者**：希望提高工作效率並降低拒絕索賠的風險。
- **醫療提供者**：需要準確的保險覆蓋信息以便於病人就診。

# User Pain Points
- 長時間的等待和繁瑣的自動菜單導航。
- 高風險的索賠拒絕，導致財務損失。
- 缺乏準確的保險覆蓋信息，影響病人就診計劃。

# Value Proposition
Donedial 提供一個自動化的語音助手，能夠在病人到診所之前完成保險查詢，快速返回保險覆蓋狀態、個人自付費用和潛在的拒絕風險，從而提高診所的工作效率並降低財務風險。

# Core Use Cases & User Stories
1. **保險查詢自動化**：
   - 作為前台人員，我希望能夠將病人的姓名和保險計劃輸入系統，讓 Donedial 自動撥打保險公司電話並返回信息。
   
2. **實時更新與學習**：
   - 作為診所管理者，我希望 Donedial 能夠隨著使用次數的增加，自動學習保險公司的菜單路徑，從而提高查詢的準確性。

# MVP Scope (Must-have vs Nice-to-have)
## Must-have
- 語音助手能夠自動撥打保險公司電話。
- 能夠導航自動菜單並返回保險覆蓋信息。
- 提供用戶友好的界面以輸入病人信息。

## Nice-to-have
- 整合多家保險公司的數據庫以提高查詢準確性。
- 提供查詢歷史和報告功能，幫助管理者分析數據。

# User Flow Overview
1. 前台人員在 Donedial 儀表板上輸入病人姓名和保險計劃。
2. Donedial 自動撥打保險公司電話，導航自動菜單。
3. 系統返回保險覆蓋狀態和自付費用，並顯示在儀表板上。
4. 前台人員根據返回的信息安排病人就診。

# Basic System Architecture
- **技術棧建議**：
  - 前端：React.js
  - 後端：Node.js + Express
  - 數據庫：MongoDB
  - 語音處理：Google Cloud Speech-to-Text API
  - 自然語言處理：Dialogflow

# Monetization Hypothesis
Donedial 可以通過訂閱模式向診所收取月費，根據使用量提供不同的計劃，並可能考慮與保險公司合作以獲取佣金。

# Success Metrics
- 每月活躍用戶數量。
- 每個用戶每月的保險查詢次數。
- 減少的索賠拒絕率。
- 用戶滿意度調查結果。

# Risks & Assumptions
- **風險**：保險公司的自動菜單可能隨時變更，導致系統需要不斷更新。
- **假設**：診所願意投入資金以提高效率並降低拒絕索賠的風險。