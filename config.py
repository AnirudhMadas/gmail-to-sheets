SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/spreadsheets",
]

CREDENTIALS_FILE = "credentials/credentials.json"
TOKEN_FILE = "token.json"

# ✅ Put your real Google Sheet ID here
SPREADSHEET_ID = "1qV2ZUCQVza70zFvvk7t7vfrXysaRUWQnDcYrDk0nPmk"

# Your sheet tab name must match (example: Sheet1)
SHEET_RANGE = "Sheet1!A:D"

# Read from inbox + only unread
GMAIL_LABEL = "INBOX"
EMAIL_QUERY = "is:unread"

# Only fetch limited emails per run
MAX_EMAILS = 10

# State persistence file (for duplicates prevention)
STATE_FILE = "state.json"
