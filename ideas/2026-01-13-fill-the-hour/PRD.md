---
title: Fill The Hour
category: saas
tags: [automation, healthcare, scheduling, b2b]
---

# 產品名稱
Fill The Hour

# One-line Pitch
一個自動化的取消回覆系統，幫助治療師即時填補取消的預約，減少收入損失。

# Background & Problem Statement
許多獨立治療師面臨客戶臨時取消預約的問題，這不僅影響他們的收入，還浪費了原本可以服務其他客戶的時間。根據調查，治療師每年因為取消預約而損失的收入可達數千美元。現有的解決方案往往依賴手動通知，效率低下，無法及時填補空缺。

# Target Users & Personas
目標用戶為獨立治療師，特別是那些在社交媒體上抱怨無法及時填補預約空缺的專業人士。這些用戶通常時間緊迫，依賴技術來提高工作效率。

## Personas
- **Emily**：30歲，心理治療師，經常面臨客戶臨時取消，對技術敏感，尋求提高預約效率的方案。
- **James**：45歲，職業治療師，擁有多位客戶，對於收入損失感到焦慮，願意嘗試新工具來改善業務。

# User Pain Points
- 客戶臨時取消預約導致收入損失。
- 手動通知等待名單上的客戶耗時且不可靠。
- 缺乏有效的工具來管理預約和客戶溝通。

# Value Proposition
Fill The Hour 提供一個自動化系統，能夠即時通知等待名單上的客戶，快速填補取消的預約，從而幫助治療師最大化收入並提高客戶滿意度。

# Core Use Cases & User Stories
1. **取消預約通知**：當客戶取消預約時，系統自動發送短信通知等待名單上的客戶。
   - *作為一名治療師，我希望能夠自動通知等待名單上的客戶，以便快速填補空缺。*
   
2. **即時預約管理**：治療師可以通過簡單的儀表板查看即時的預約空缺。
   - *作為一名治療師，我希望能夠輕鬆查看我的預約狀態，並快速了解可用的時間。*

# MVP Scope
## Must-have
- 與 SimplePractice 和 TherapyNotes 的API集成。
- 簡單的儀表板顯示即時預約空缺。
- 使用 Twilio 發送短信通知。

## Nice-to-have
- 客戶反饋收集功能。
- 數據分析報告，幫助治療師了解取消模式。

# User Flow Overview
1. 客戶取消預約。
2. 系統接收取消通知並查詢等待名單。
3. 系統自動發送短信給第一位等待的客戶。
4. 客戶確認預約，系統更新儀表板。

# Basic System Architecture
- **前端**：React.js 或 Vue.js
- **後端**：Node.js + Express
- **數據庫**：MongoDB 或 PostgreSQL
- **API集成**：SimplePractice API, TherapyNotes API
- **短信服務**：Twilio

# Monetization Hypothesis
每位治療師每月收費 $49-$99，對於多提供者的診所包月收費 $299。預計每位治療師至少能夠通過減少兩次無顯示的預約來回本。

# Success Metrics
- 每月活躍用戶數 (MAU)
- 客戶滿意度評分
- 每位用戶的收入增長百分比
- 預約填補率

# Risks & Assumptions
- **風險**：客戶可能對自動化通知感到厭煩，導致用戶流失。
- **假設**：治療師願意為提高預約效率支付額外費用，並且會接受新的技術解決方案。