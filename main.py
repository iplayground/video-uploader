#!/usr/bin/python
# coding: utf-8

from __future__ import print_function

import pickle
import os.path

from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import youtube_uploader

SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/drive.metadata.readonly']

load_dotenv(verbose=True)
SHEET_ID = os.getenv('GSHEET_ID')
SHEET_RANGE = os.getenv('GSHEET_RANGE')
GDRIVE_ID = os.getenv('GDRIVE_ID')


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Setup Sheet
    g_sheet_service = build('sheets', 'v4', credentials=creds)
    sheet = g_sheet_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID,
                                range=SHEET_RANGE).execute()
    sheet_values = result.get('values', [])

    # Setup GDrive
    g_drive_service = build('drive', 'v3', credentials=creds)
    results = g_drive_service.files().list(
        fields='nextPageToken, files(id, name)',
        includeItemsFromAllDrives=True,
        driveId=GDRIVE_ID,
    ).execute()
    g_drive_values = results.get('files', [])

    if not sheet_values:
        print('No data found.')
    else:
        print('Sheet Values:')
        for row in sheet_values:
            print(row)

        print('GDrive list:')
        for item in g_drive_values:
            print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()
