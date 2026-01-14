# Gmail to Google Sheets Automation (Python)
**Author:** Anirudh Madas

📌 Internship Project Assignment  
This project connects to the **Gmail API** and **Google Sheets API** using **OAuth 2.0** and logs **unread inbox emails** into a Google Sheet. After processing, each email is marked as **read**.

---

## 📖 Project Overview
The goal of this automation is to read real incoming emails from my Gmail inbox and store them as structured rows in Google Sheets.

Each qualifying email is appended as a new row with the following fields:

| Column Name | Description |
|------------|-------------|
| From       | Sender email address |
| Subject    | Email subject |
| Date       | Date & time received |
| Content    | Email body (plain text) |

---

## 🧠 High-Level Architecture Diagram

                   ┌───────────────────────────────┐
                   │           config.py           │
                   │  - SCOPES                     │
                   │  - Spreadsheet ID             │
                   │  - Sheet Range                │
                   │  - File paths                 │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
    ┌────────────────────────────────────────────────────────────────────┐
    │                            main.py                                 │
    │                    (Orchestrator / Controller)                     │
    │                                                                    │
    │  1) Connect Gmail API  → get_gmail_service()                       │
    │  2) Connect Sheets API → get_sheets_service()                      │
    │  3) Load state.json (processed_ids)                                │
    │  4) Fetch unread emails from Inbox                                 │
    │  5) For each email:                                                │
    │        - parse email                                               │
    │        - append row to sheet                                       │
    │        - mark email as READ                                        │
    │        - save processed_id to state.json                           │
    └───────────────┬───────────────────────┬────────────────────────────┘
                    │                       │
                    │                       │
                    ▼                       ▼
    ┌──────────────────────────┐   ┌──────────────────────────┐
    │     gmail_service.py     │   │    sheets_service.py     │
    │   (Gmail API Handling)   │   │  (Google Sheets Writing) │
    │                          │   │                          │
    │ - OAuth login/token      │   │ - Build Sheets service   │
    │ - Fetch unread messages  │   │ - Append row to sheet    │
    │ - Get email full data    │   │                          │
    │ - Mark email as read     │   │                          │
    └───────────────┬──────────┘   └───────────────┬──────────┘
                    │                              │
                    ▼                              ▼
      ┌───────────────────┐          ┌────────────────────────┐
      │   Gmail Inbox     │          │      Google Sheet      │
      │ (Unread emails)   │          │ (Email log database)   │
      └───────────────────┘          └────────────────────────┘

                ▲
                │
                │
     ┌──────────┴────────────┐
     │   email_parser.py     │
     │ (Extract From/Subject │
     │  Date/Content)        │
     └───────────────────────┘


         ┌──────────────────────────────────────────┐
         │         state.json (Local Storage)       │
         │   - stores processed message IDs         │
         │   - prevents duplicates across runs      │
         └──────────────────────────────────────────┘


## 📂 Required Project Structure

gmail-to-sheets/

│

├── src/

│ ├── gmail_service.py

│ ├── sheets_service.py

│ ├── email_parser.py

│ └── main.py

│

├── credentials/

│ └── credentials.json (DO NOT COMMIT)

│

├── .gitignore

├── requirements.txt

├── README.md

└── config.py



---

## ✅ Technical Requirements Met

- ✅ Python 3
- ✅ Gmail API integration
- ✅ Google Sheets API integration
- ✅ OAuth 2.0 authentication (no service accounts)
- ✅ Reads emails from:
  - Inbox ✅
  - Unread only ✅
- ✅ Appends only new emails since previous run
- ✅ Prevents duplicate rows
- ✅ Marks emails as read after processing

---

## ⚙️ Step-by-Step Setup Instructions

### 1️⃣ Create a Google Cloud Project
1. Go to Google Cloud Console
2. Create a new project

### 2️⃣ Enable Required APIs
Enable these APIs:
- Gmail API
- Google Sheets API

### 3️⃣ Configure OAuth Consent Screen
1. Go to **APIs & Services → OAuth consent screen**
2. Choose **External**
3. Fill App Name + Email
4. Save

✅ If in **Testing mode**, add your Gmail to **Test Users**.

### 4️⃣ Create OAuth Client Credentials
1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth Client ID**
3. Choose **Desktop App**
4. Download the `credentials.json`

Place it here:


credentials/credentials.json


### 5️⃣ Create a Google Sheet
1. Create a new Google Sheet
2. Add headers in Row 1:

| From | Subject | Date | Content |

3. Copy Spreadsheet ID from URL:


https://docs.google.com/spreadsheets/d/
<SPREADSHEET_ID>/edit


Update `config.py`:
```python
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"
SHEET_RANGE = "Sheet1!A:D"
```
### 6️⃣ Install Dependencies
pip install -r requirements.txt

### 7️⃣ Run the Script

From project root:

```python
python -m src.main
```

✅ First run will open a browser for OAuth login

✅ After successful login, a token.json file is created automatically


## 🔐 OAuth Flow Used (Explanation)

### This project uses OAuth 2.0 Installed App Flow:

Script opens a Google Login URL in browser

User signs in and grants permissions

Google redirects to localhost with an authorization code

The script exchanges the code for an access token

The token is stored in token.json and reused for next runs

✅ This follows the assignment rule: OAuth 2.0 (no service accounts)

## 🚫 Duplicate Prevention Logic

Duplicate rows are prevented using the Gmail message_id.

Every processed email has a unique message_id

The script stores processed IDs locally

If an email ID was already processed earlier, it is skipped

This ensures:

✅ No duplicate rows

✅ Re-running script does not re-log older emails


## 💾 State Persistence Method (How & Why)

State is stored in a local JSON file:

### 📌 state.json

Example:

```python
{
  "processed_ids": [
    "18d92f0a2b19c123",
    "18d92f1c33b4a999"
  ]
}
```
### ✅ Why this approach?

Simple and lightweight

Works offline

No external database needed

Prevents duplicates even if emails are still unread due to crash

### ✅ Email Scope & Processing Rules

This script only reads:

Inbox emails

Unread emails only

After processing and logging to Sheets:

### ✅ The script marks the email as READ

This ensures the next run focuses only on new unread emails.

## 🧩 Challenge Faced & How I Solved It

### ✅ Challenge: Google Sheets cell limit error (50,000 characters)

Some emails have very large content (long HTML/template emails).

Google Sheets has a maximum limit of 50,000 characters per cell, which caused an API error.

### ✅ Solution:

Extract plain text content

Truncate content if it exceeds the allowed limit

Append safely without crashing the app

### ⚠️ Limitations of This Solution

Real-time push notifications are not implemented (polling/run-based execution)

If email body is extremely large, the content may be truncated to fit Sheets limits

HTML-to-text conversion is minimal (plain text extraction only)

Logging with timestamps
