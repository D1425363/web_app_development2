# 流程圖設計：數位食譜管理平台

## 1. 使用者流程圖（User Flow）

以下流程圖展示了使用者在平台上進行主要操作的路徑，涵蓋食譜的瀏覽、新增、檢視、編輯及刪除等核心功能。

```mermaid
flowchart LR
    Start([使用者開啟網頁]) --> Home[首頁 - 食譜列表]
    
    Home --> Action{選擇操作}
    
    Action -->|瀏覽食譜| ViewList[依分類或標籤檢索]
    ViewList --> Detail[查看食譜詳細內容]
    
    Action -->|新增食譜| CreateForm[進入新增食譜表單]
    CreateForm --> FillCreate[填寫名稱、材料、步驟與標籤]
    FillCreate --> SubmitCreate[送出儲存]
    SubmitCreate --> Detail
    
    Detail --> DetailAction{進階操作}
    DetailAction -->|編輯食譜| EditForm[進入編輯表單]
    EditForm --> FillEdit[修改食譜內容]
    FillEdit --> SubmitEdit[送出更新]
    SubmitEdit --> Detail
    
    DetailAction -->|刪除食譜| ConfirmDelete[確認刪除]
    ConfirmDelete --> DeleteSuccess[刪除成功]
    DeleteSuccess --> Home
    
    DetailAction -->|生成購物清單| ShoppingList[顯示材料購物清單]
    
    DetailAction -->|新增筆記評價| NoteForm[填寫實作筆記與評價]
    NoteForm --> SubmitNote[儲存筆記]
    SubmitNote --> Detail
```

## 2. 系統序列圖（Sequence Diagram）

以下序列圖描述「使用者點擊新增食譜」到「資料存入資料庫」的完整技術流程：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Database Model
    participant DB as SQLite 資料庫

    User->>Browser: 填寫新增食譜表單並點擊「送出」
    Browser->>Route: POST /recipes/new (攜帶表單資料)
    
    Route->>Route: 驗證資料格式 (如: 必填欄位)
    
    alt 資料驗證成功
        Route->>Model: 呼叫新增食譜方法 (傳遞資料)
        Model->>DB: 執行 INSERT INTO recipes ...
        DB-->>Model: 回傳成功狀態與新食譜 ID
        Model-->>Route: 確認寫入成功
        Route-->>Browser: HTTP 302 重導向至 /recipes/{id} (食譜詳細頁)
        Browser->>User: 顯示剛建立的食譜畫面
    else 資料驗證失敗
        Route-->>Browser: 回傳原本表單頁面 (附帶錯誤訊息)
        Browser->>User: 顯示請重新填寫的提示
    end
```

## 3. 功能清單對照表

根據系統功能，我們初步規劃以下的 URL 路徑與對應的 HTTP 請求方法：

| 功能項目 | HTTP 方法 | URL 路徑 | 說明 |
| --- | --- | --- | --- |
| **瀏覽食譜列表** | GET | `/` 或 `/recipes` | 顯示所有食譜，支援分類標籤檢索 |
| **查看食譜詳情** | GET | `/recipes/<int:id>` | 顯示單一食譜的詳細步驟、材料與筆記 |
| **新增食譜 (表單)** | GET | `/recipes/new` | 顯示用來新增食譜的空白表單 |
| **新增食譜 (處理)** | POST | `/recipes/new` | 接收表單資料並存入資料庫 |
| **編輯食譜 (表單)** | GET | `/recipes/<int:id>/edit` | 顯示帶有原資料的表單供修改 |
| **編輯食譜 (處理)** | POST | `/recipes/<int:id>/edit` | 接收修改後的資料並更新資料庫 |
| **刪除食譜** | POST | `/recipes/<int:id>/delete` | 從資料庫中刪除該筆食譜資料 |
| **生成購物清單** | GET | `/recipes/<int:id>/shopping-list` | 擷取食譜材料並整理成購物清單 |
| **新增筆記評價** | POST | `/recipes/<int:id>/notes` | 將實作筆記與評價附加到指定食譜 |
