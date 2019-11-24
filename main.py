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
          'https://www.googleapis.com/auth/drive.readonly']

load_dotenv(verbose=True)
SHEET_ID = os.getenv('GSHEET_ID')
SHEET_RANGE = os.getenv('GSHEET_RANGE')


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

    g_sheet_service = build('sheets', 'v4', credentials=creds)
    sheet = g_sheet_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID,
                                range=SHEET_RANGE).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Sheet Values:')
        for row in values:
            print(row)
        # for row in values:
        #     # Print columns A and E, which correspond to indices 0 and 4.
        #     print('%s, %s' % (row[0], row[4]))


if __name__ == '__main__':
    main()
