from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')
COLUMN_RANGE = 'Sheet1!B:B'


def authenticate_google_sheets():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=creds)


def find_next_empty_row(service):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=COLUMN_RANGE).execute()
    return len(result.get('values', [])) + 1


def write_to_google_sheet(service, row, score):
    range_name = f'Sheet1!B{row}'
    values = [[score]]
    body = {'values': values}
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption='RAW', body=body).execute()
    print(f"{result.get('updatedCells')} cells updated.")


def main(score):
    service = authenticate_google_sheets()
    next_empty_row = find_next_empty_row(service)
    write_to_google_sheet(service, next_empty_row, score)


if __name__ == '__main__':
    main()
