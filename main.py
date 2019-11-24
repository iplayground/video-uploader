#!/usr/bin/python
# coding: utf-8

from __future__ import print_function

import pickle
import subprocess
import os.path

from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import youtube_uploader

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

load_dotenv(verbose=True)
SHEET_ID = os.getenv('GSHEET_ID')
SHEET_RANGE = os.getenv('GSHEET_RANGE')
DOWNLAOD_PATH = os.getenv('TEMP_FOLDER')


def download_video(url, path):
    subprocess.run(['youtube-dl',
                    "-o %s '%s'".format(path, url)],
                   shell=True)


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
    result = sheet.values().get(
        spreadsheetId=SHEET_ID,
        range=SHEET_RANGE,
    ).execute()
    sheet_values = result.get('values', [])

    if not sheet_values:
        print('No data found.')
    else:
        print('Sheet Values:')
        for row in sheet_values:
            # print(row)
            fileName = row[0]
            url = None
            if len(row) >= 7:
                url = row[7]
            print("file:%s uploaded:%s videoURL:%s" % (fileName, row[5], url))

            filePath = '{}%(title)s.mp4'.format(DOWNLAOD_PATH)
            if os.path.exists(filePath):
                print('Upload %s' % (fileName))
            elif url is not None:
                print("Downlaod {}".format(url))
                download_video(url, filePath)


if __name__ == '__main__':
    main()
