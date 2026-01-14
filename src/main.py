import json
import os

from config import STATE_FILE
from src.gmail_services import (
    get_gmail_service,
    fetch_unread_emails,
    get_message,
    mark_as_read
)
from src.sheets_services import get_sheets_service, append_row
from src.email_parser import parse_email


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"processed_ids": []}

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def main():
    print("✅ Starting Gmail → Sheets Automation...")

    gmail_service = get_gmail_service()
    creds = gmail_service._http.credentials
    sheets_service = get_sheets_service(creds)

    state = load_state()
    processed_ids = set(state.get("processed_ids", []))

    unread_messages = fetch_unread_emails(gmail_service)

    if not unread_messages:
        print("📭 No unread emails found.")
        return

    print(f"📩 Found {len(unread_messages)} unread emails...")

    for item in unread_messages:
        message_id = item["id"]

        # ✅ duplicate prevention
        if message_id in processed_ids:
            print(f"⚠ Skipping duplicate email (already processed): {message_id}")
            continue

        try:
            msg = get_message(gmail_service, message_id)

            # parse row: From, Subject, Date, Content
            row = parse_email(msg)

            # append to sheet
            append_row(sheets_service, row)
            print(f"✅ Logged email: {row[1]}")  # Subject

            # mark as read
            mark_as_read(gmail_service, message_id)
            print("✔ Marked as READ")

            # save state
            processed_ids.add(message_id)
            state["processed_ids"] = list(processed_ids)
            save_state(state)

        except Exception as e:
            print(f"❌ Error processing email ID {message_id}: {e}")

    print("🎉 Done! All emails processed.")


if __name__ == "__main__":
    main()
