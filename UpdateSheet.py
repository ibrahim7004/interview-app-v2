from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Constants
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'sorsx-sheets-credentials.json'
SPREADSHEET_ID = '18iwFkn6PasXuckVZxUc3DgCW9OohTs0kjcqGibrPhO4'
COLUMN_RANGE = 'Sheet1!B:B'


def authenticate_google_sheets():
    """Authenticate and return the Google Sheets service instance."""
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=creds)


def find_next_empty_row(service):
    """Find the next empty row in the specified column range."""
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=COLUMN_RANGE).execute()
    return len(result.get('values', [])) + 1


def write_to_google_sheet(service, row, score):
    """Write the score to the next empty row in the Google Sheet."""
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
