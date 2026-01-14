import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from config import (
    SCOPES,
    CREDENTIALS_FILE,
    TOKEN_FILE,
    GMAIL_LABEL,
    EMAIL_QUERY,
    MAX_EMAILS,
)

def get_gmail_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def fetch_unread_emails(service):
    results = service.users().messages().list(
        userId="me",
        labelIds=[GMAIL_LABEL],
        q=EMAIL_QUERY,
        maxResults=MAX_EMAILS
    ).execute()

    return results.get("messages", [])


def get_message(service, message_id):
    return service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()


def mark_as_read(service, message_id):
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()
