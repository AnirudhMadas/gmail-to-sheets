import base64
MAX_CELL_CHARS = 45000

def _get_header(headers, name):
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def _decode_base64(data):
    if not data:
        return ""
    decoded_bytes = base64.urlsafe_b64decode(data.encode("utf-8"))
    return decoded_bytes.decode("utf-8", errors="ignore")


def _extract_plain_text(payload):
    """
    Gmail emails can be:
    - plain text only
    - html only
    - multipart with different parts
    We want best possible plain text.
    """
    if not payload:
        return ""

    mime_type = payload.get("mimeType", "")
    body = payload.get("body", {})
    data = body.get("data")

    if mime_type == "text/plain" and data:
        return _decode_base64(data)

    parts = payload.get("parts", [])
    for part in parts:
        part_mime = part.get("mimeType", "")
        part_body = part.get("body", {})
        part_data = part_body.get("data")

        if part_mime == "text/plain" and part_data:
            return _decode_base64(part_data)

    if data:
        return _decode_base64(data)

    return ""


def parse_email(message):
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    sender = _get_header(headers, "From")
    subject = _get_header(headers, "Subject")
    date = _get_header(headers, "Date")
    content = _extract_plain_text(payload)

    if len(content) > MAX_CELL_CHARS:
        content = content[:MAX_CELL_CHARS] + "\n\n...[TRUNCATED]"

    return [sender, subject, date, content]
