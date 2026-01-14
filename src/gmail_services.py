import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE, GMAIL_LABEL


def get_gmail_service():
    creds = None

    # Load token if exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If token missing/expired, create new
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def list_unread_emails(service, max_results=10):
    """
    Fetch unread emails from inbox.
    """
    results = service.users().messages().list(
        userId="me",
        labelIds=[GMAIL_LABEL],
        q="is:unread",
        maxResults=max_results
    ).execute()

    return results.get("messages", [])


def get_email_detail(service, message_id):
    """
    Get full email data by id.
    """
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    return message


def mark_email_as_read(service, message_id):
    """
    Remove UNREAD label from email
    """
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={
            "removeLabelIds": ["UNREAD"]
        }
    ).execute()
