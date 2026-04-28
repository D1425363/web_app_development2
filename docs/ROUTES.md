# 路由設計文件：數位食譜管理平台

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 / 食譜列表 | GET | `/` 或 `/recipes` | `templates/recipes/index.html` | 顯示所有食譜，支援標籤搜尋 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/recipes/new.html` | 顯示新增食譜與材料步驟表單 |
| 建立食譜 | POST | `/recipes/new` | — | 接收表單，存入 DB，重導向至首頁或詳情頁 |
| 食譜詳情 | GET | `/recipes/<id>` | `templates/recipes/detail.html` | 顯示單筆食譜、材料、步驟與筆記 |
| 編輯食譜頁面 | GET | `/recipes/<id>/edit` | `templates/recipes/edit.html` | 顯示編輯表單 |
| 更新食譜 | POST | `/recipes/<id>/edit` | — | 接收表單，更新 DB，重導向至詳情頁 |
| 刪除食譜 | POST | `/recipes/<id>/delete` | — | 刪除後重導向至首頁 |
| 新增筆記 | POST | `/recipes/<id>/notes` | — | 接收筆記表單，寫入 DB，重導向至詳情頁 |
| 產生購物清單 | GET | `/recipes/<id>/shopping-list` | `templates/recipes/shopping_list.html` | 顯示該食譜所需的材料清單 |

## 2. 每個路由的詳細說明

### 首頁 / 食譜列表
- **路由**: `GET /recipes`
- **輸入**: 可選 URL 參數 `?tag=xxx` 用於標籤過濾。
- **處理邏輯**: 呼叫 `Recipe.get_all()`，若有 `tag` 則在 Python 進行過濾或修改 Model 提供搜尋方法。
- **輸出**: 渲染 `recipes/index.html`。
- **錯誤處理**: 無特殊錯誤。

### 新增食譜
- **頁面**: `GET /recipes/new`
  - 輸出: 渲染 `recipes/new.html`
- **建立**: `POST /recipes/new`
  - 輸入: 表單欄位 `title`, `description`, `tags`, 陣列形式的材料 (`ingredients[]`, `amounts[]`), 陣列形式的步驟 (`instructions[]`)。
  - 處理邏輯: 
    1. 呼叫 `Recipe.create()` 取得 `recipe_id`。
    2. 迴圈呼叫 `Ingredient.create()` 與 `Step.create()`。
  - 輸出: 重導向到 `/recipes/<recipe_id>`。
  - 錯誤處理: 必填欄位若空，則導回表單並顯示錯誤訊息。

### 食譜詳情
- **路由**: `GET /recipes/<id>`
- **輸入**: URL 參數 `<id>`。
- **處理邏輯**: 呼叫 `Recipe.get_by_id()`, `Ingredient.get_by_recipe()`, `Step.get_by_recipe()`, `Note.get_by_recipe()`。
- **輸出**: 渲染 `recipes/detail.html`。
- **錯誤處理**: 若 `Recipe.get_by_id()` 回傳 None，回傳 404 錯誤頁面。

### 編輯食譜
- **頁面**: `GET /recipes/<id>/edit`
  - 輸入: URL 參數 `<id>`。
  - 處理邏輯: 取得當前食譜的所有資料並帶入表單。
  - 輸出: 渲染 `recipes/edit.html`。
- **更新**: `POST /recipes/<id>/edit`
  - 輸入: 表單修改後的食譜、材料與步驟資料。
  - 處理邏輯: 
    1. 呼叫 `Recipe.update()`。
    2. 呼叫 `Ingredient.delete_by_recipe()` 與 `Step.delete_by_recipe()`。
    3. 重新呼叫 `Ingredient.create()` 與 `Step.create()` 寫入新資料。
  - 輸出: 重導向到 `/recipes/<id>`。

### 刪除食譜
- **路由**: `POST /recipes/<id>/delete`
- **處理邏輯**: 呼叫 `Recipe.delete()` (設定 CASCADE 會自動刪除關聯資料)。
- **輸出**: 重導向到 `/recipes`。

### 新增筆記與評價
- **路由**: `POST /recipes/<id>/notes`
- **輸入**: 表單欄位 `content`, `rating`。
- **處理邏輯**: 呼叫 `Note.create()`。
- **輸出**: 重導向到 `/recipes/<id>` 顯示最新筆記。

### 購物清單
- **路由**: `GET /recipes/<id>/shopping-list`
- **處理邏輯**: 呼叫 `Ingredient.get_by_recipe()` 取得材料。
- **輸出**: 渲染 `recipes/shopping_list.html`。

## 3. Jinja2 模板清單

所有頁面皆繼承自 `base.html`，以保持共同的導覽列與外觀。

- `base.html`：母版，包含 Navbar (導覽列) 與 Footer。
- `recipes/index.html`：食譜列表，卡片式呈現。
- `recipes/detail.html`：食譜詳細內容頁，包含筆記顯示與新增筆記的區塊。
- `recipes/new.html`：新增食譜用的表單。
- `recipes/edit.html`：編輯食譜用的表單。
- `recipes/shopping_list.html`：簡單的購物清單列印或檢視頁面。

## 4. 路由骨架程式碼
已在 `app/routes/` 建立相關骨架檔案：
- `app/routes/recipe_routes.py`
