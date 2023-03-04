# getservice(): Authorize access to Google Docs
# main(): Get content from a Google Doc--(1) in JSON form, (2) in text form
# CITATION: Google Docs API quickstart

from __future__ import print_function  # not sure what this does

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# from googleapiclient.discovery import build
import googleapiclient.discovery
from googleapiclient.errors import HttpError

import mytest
import pyperclip
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0'


# Authorizes the user to access Google Docs
# TODO: add SCOPES as an optional variable, delete token.json if it is being changed
# CITATION: Google Docs API quickstart
def getservice():
    """Credentials testing"""
    creds = None

    # The file token.json stores the user's access and refresh tokens.
    # Created automatically when the authorization flow completes for the first time.
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../token.json', 'w') as token:
            token.write(creds.to_json())

    # Create + return "service", which you can use to access the Docs API
    try:
        service = googleapiclient.discovery.build('docs', 'v1', credentials=creds)
    except HttpError as err:
        print(err)

    return service


# # Get content from a Google Doc--(1) in JSON form, (2) in text form
# # CITATION: Google Docs API quickstart
# def quickstart():
#     """Credentials testing (boilerplate)
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens.
#     # Created automatically when the authorization flow completes for the first time.
#     if os.path.exists('../token.json'):
#         creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 '../credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('../token.json', 'w') as token:
#             token.write(creds.to_json())


#     try:
#         service = build('docs', 'v1', credentials=creds)

#         # Retrieve the documents contents from the Docs service.
#         document = service.documents().get(documentId=DOCUMENT_ID).execute()

#         # TEST Check the contents of the document
#         print('The title of the document is: {}'.format(document.get('title')))
#         # print('The body of the document is:\n{}'.format(document.get('body')))
#         # print(json.dumps(document.get('body'), indent=4))

#         #PERSONAL REF:
#         #document.get('body') is a dictionary with one entry, "content"
#         #content contains a list of dictionaries
#             #fist dict in the list talks about styles and whatnot
#             #second dict has the element "paragraph"
#                 # "paragraph" is a dict containing "elements"
#                     # elements is a list. its first entry is a dict
#                         # the first dict in "elements" had an entry, "content"
#                         # the value of "content" is the first line
#         # firstline = document.get('body')['content'][1]['paragraph']['elements'][0]['textRun']['content']

#         # Get content
#         doclines = document.get('body')['content']
#         content = ""
#         for line in doclines[1:]:
#             content += line['paragraph']['elements'][0]['textRun']['content']

#         # Copy content, move to "tester" function
#         pyperclip.copy(content)
#         print(mytest.tester())


#     except HttpError as err:
#         print(err)


# if __name__ == '__main__':
#     quickstart()
