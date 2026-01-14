import base64


def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def extract_email_data(message):
    """
    Extract useful info from Gmail message response.
    Returns: [date, from, subject, snippet, message_id]
    """
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    sender = get_header(headers, "From")
    subject = get_header(headers, "Subject")
    date = get_header(headers, "Date")
    snippet = message.get("snippet", "")
    message_id = message.get("id")

    return [date, sender, subject, snippet, message_id]
