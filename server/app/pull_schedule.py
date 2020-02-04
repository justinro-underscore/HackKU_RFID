from __future__ import print_function
import pickle
import os.path
import json
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_schedule():
    if not os.path.exists('../local_data/google_sheets_id.txt'):
        raise Exception("Error: must have google sheets ID file")

    with open('../local_data/google_sheets_id.txt', 'r') as f:
        sheets_id = f.read()

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = sheets_id
    RANGE_NAME = "Run of Show!A1:F"

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../local_data/token.pickle'):
        with open('../local_data/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../local_data/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../local_data/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        return None

    current_day = ""
    events = []
    for row in values[1:]:
        if len(row) == 1:
            current_day = row[0]
        else:
            if row[5] == "Yes":
                if "-" in row[0]:
                    time = datetime.strptime(current_day + ": " + row[0].split(" - ")[0], "%A %b %d, %Y: %I:%M %p")
                else:
                    time = datetime.strptime(current_day + ": " + row[0], "%A %b %d, %Y: %I:%M %p")
                event = {
                    "name": row[3],
                    "time": time,
                    "location": row[4]
                }
                events.append(event)
    print("Events retrieved successfully!")
    return events
