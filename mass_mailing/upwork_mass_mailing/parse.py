from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def parse_sheet(sheet_id):
    """
    parses the spreadsheet
    returns an array [[human], [human]...] where human:
    [0] - fName
    [1] -lName
    [2] - email
    """

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = sheet_id[0].decode('utf-8')
    SAMPLE_RANGE_NAME = 'Mail Merge!A2:D'
    creds = None
    # You should add credentials.json to this folder if it is not added
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    final = []
    if not values:
        print('No data found.')
        return []
    else:
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            # Append a human to list
            print(row)
            final.append([row[i] for i in range(len(row))])
        return final


if __name__ == '__main__':
    raise NotImplementedError
