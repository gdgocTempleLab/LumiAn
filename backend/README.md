# LumiAn Backend API

本專案為 LumiAn 系統之後端 API 服務，主要基於 Django 框架與 Django REST Framework (DRF) 建立。為保持輕量化並符合前後端分離，此專案已**全面關閉 Django 預設的 UI 渲染與後台介面**，所有端點皆為純 JSON 格式的 API。

## ⚙️ 環境建置 (Setup)

### 1. 建立與啟動虛擬環境
本專案不包含虛擬環境實體檔案，開發前需先自行建立 Python 虛擬環境（建議命名為 `.env`）。請在終端機中切換到專案根目錄，並依序執行以下指令：

**建立虛擬環境：**
```bash
python -m venv .env
```

**啟動虛擬環境：**
- **Windows (PowerShell)**:
  ```powershell
  .\.env\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  source .env/bin/activate
  ```

### 2. 安裝相依套件
進入 `backend` 目錄後，安裝 `requirements.txt` 中所列的必備清單：
```bash
cd backend
pip install -r requirements.txt
```

> [!NOTE]  
> 專案依賴包含了 `django`, `djangorestframework`, 以及 `djangorestframework-simplejwt` 以利發送與驗證 JWT Token。

---

## 🗄️ 資料庫設定 (Database)

本系統目前預設使用 SQLite (`db.sqlite3`)。

### 1. 執行遷移檔 (Migration)
確保資料表的建立與更新。
```bash
python manage.py migrate
```

### 2. 建立最高權限管理員 (Superuser)
若您需要建立一個全新的管理員帳號：
```bash
python manage.py createsuperuser
```
*(注意：開發階段目前資料庫裡預設已有一組帳號 `test_user` / 密碼 `testpasswd` 供快速測試使用。)*

---

## 🚀 啟動伺服器 (Running the Server)

確定身處在 `backend` 目錄中，並執行以下指令來啟動開發伺服器：
```bash
python manage.py runserver
```

伺服器成功啟動後，將會在此位址監聽請求：`http://127.0.0.1:8000/`

---

## 🏗️ 專案架構與 API

本專案規畫依照業務邏輯切分為多個 Django Apps，目前已建立的包含：

- `lumian`: 系統核心設定層（Settings, Root URLs）。
- `system`: 系統底層行為模組。包含登入 API 與系統級操作。

### 測試登入 API 

伺服器運行後，可發送 POST 請求至 `http://127.0.0.1:8000/api/sys/login/`：

**Request Body (JSON):**
```json
{
  "Data": {
    "Account": "test_user",
    "Password": "testpasswd"
  }
}
```

**Response (JSON):**
```json
{
  "Status": "Success",
  "Data": {
    "AccessToken": "eyJhbGciOiJIUzI1NiIsInR..."
  }
}
```
> [!TIP]  
> `AccessToken` payload 內部夾帶了使用者的身分識別標籤 (`role`)，前端可解析該 Token 取出對應的角色權限（如 `"Admin"`、`"User"`）。

> [!WARNING]
> **安全性指引 (Security Guideline)**  
> 預設的 `test_user` 帳密僅作為初次跑通登入流程的範例。**在完成初次登入測試後，請務必引導使用者/開發者進行「更改密碼」的相關測試與操作**（可透過開發對應的 Change Password API 或直接使用指令 `python manage.py changepassword test_user` 進行修改），以嚴格確保系統在後續開發及部署階段的安全性！
