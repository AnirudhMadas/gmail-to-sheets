from src.gmail_services import (
    get_gmail_service,
    list_unread_emails,
    get_email_detail,
    mark_email_as_read
)

from src.email_parser import extract_email_data
from src.sheets_services import get_sheets_service, append_row



def main():
    print("✅ Starting Gmail → Sheets Automation...")

    gmail_service = get_gmail_service()

    # creds inside gmail_service are stored internally,
    # but easiest way: rebuild sheets using same gmail creds
    creds = gmail_service._http.credentials
    sheets_service = get_sheets_service(creds)

    unread_emails = list_unread_emails(gmail_service, max_results=10)

    if not unread_emails:
        print("📭 No unread emails found.")
        return

    print(f"📩 Found {len(unread_emails)} unread emails...")

    for msg in unread_emails:
        message_id = msg["id"]

        # Fetch full email
        email_message = get_email_detail(gmail_service, message_id)

        # Parse email into sheet row
        row = extract_email_data(email_message)

        # Append to Google Sheet
        append_row(sheets_service, row)
        print(f"✅ Logged email: {row[2]}")

        # Mark email as read
        mark_email_as_read(gmail_service, message_id)
        print("✔ Marked as read\n")

    print("🎉 Done! All unread emails logged.")


if __name__ == "__main__":
    main()
