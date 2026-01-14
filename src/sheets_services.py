from googleapiclient.discovery import build
from config import SPREADSHEET_ID, SHEET_RANGE


def get_sheets_service(creds):
    return build("sheets", "v4", credentials=creds)


def append_row(service, row):
    body = {"values": [row]}

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_RANGE,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
