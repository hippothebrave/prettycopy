import pyperclip
import re
from googleapiclient.errors import HttpError

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import googleapiclient.discovery

# PUBLIC FUNCTIONS


def nonewlines(text=None):
    """Remove all newlines.

    Takes in a text input from the argument or (by default) the clipboard, removes all newlines,
    and recopies it to the clipboard.

    Args:
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.

    """
    if text is None:
        text = pyperclip.paste()
    if not isinstance(text, str):
        raise ValueError("PrettyCopy can only take in strings!")

    text = ' '.join([line.strip() for line in text.split()])
    pyperclip.copy(text)
    return text


def nobullets(text=None):
    """Take out old newlines, replace bullets with newlines.

    Takes in a text input from the argument or (by default) the clipboard. Removes all newlines,
    and replaces any bullet symbols with newlines.

    Args:
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.

    """
    if text is None:
        text = pyperclip.paste()
    if not isinstance(text, str):
        raise ValueError("PrettyCopy can only take in strings!")

    text = nonewlines().strip("• ")
    text = re.sub(r"\s*•\s*", "\n", text)
    pyperclip.copy(text)
    return text


def bullettopar(text=None):
    """Remove newlines, replace bullets with spaces

    Takes in a text input from the argument or (by default) the clipboard. Removes all newlines,
    and replaces any bullet symbols with a space.

    Args:
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.

    """
    if text is None:
        text = pyperclip.paste()
    if not isinstance(text, str):
        raise ValueError("PrettyCopy can only take in strings!")

    text = ' '.join([line.strip() for line in text.split()]).strip("• ")
    text = re.sub(r"\s*•\s*", " ", text)
    pyperclip.copy(text)
    return text


def simplequote(text=None):
    """Add quotes around clipboard contents.

    Adds quotation marks around a text input from the argument or (by default) the clipboard.

    Args:
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.

    """
    if text is None:
        text = pyperclip.paste()
    if not isinstance(text, str):
        raise ValueError("PrettyCopy can only take in strings!")

    text = '"' + text + '"'
    pyperclip.copy(text)
    return text


def quote(end_punctuation=None, text=None):
    """Add quotes (and optional comma) around clipboard contents.

    Adds quotation marks and end punctuation to a text input from the argument or (by default) the clipboard.

    Args:
        end_punctuation (str): A single-character string containing one of: [.,!?]
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.

    """
    if text is None:
        text = pyperclip.paste()
    if not isinstance(text, str):
        raise ValueError("PrettyCopy can only take in strings!")

    if end_punctuation is not None:
        if len(end_punctuation) != 1:
            raise ValueError("End punctuation should be a single character.")
        elif end_punctuation not in [',', '.', '!', '?']:
            raise ValueError("End punctuation should be one of: [.,!?]")
        text = '"' + text + end_punctuation + '"'
    else:
        text = '"' + text + ',"'
    pyperclip.copy(text)
    return text


def trimspacing(text=None):
    """Removes empty lines clipboard contents.

    Removes empty lines from a text input from the argument or (by default) the clipboard.

    Args:
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.
    """
    if text is None:
        text = pyperclip.paste()
    if not isinstance(text, str):
        raise ValueError("PrettyCopy can only take in strings!")

    text = re.sub(r"(\r?\n)+", "\n", text)
    text = text.strip()
    pyperclip.copy(text)
    return text


# FIXME: only works if you have the document ID
# FIXME: only pastes at end of document
def betterbullets(docID):
    """Add clipboard content to end of Google Doc as a bulleted list.

    Takes text from the clipboard. Removes all newlines and replaces bullet symbols with newlines.
    Copies the text to the end of a Google Doc as a bulleted list.

    Args:
        docID (str): The ID of a Google Doc.

    Returns:
        str: Corrected text.

    """
    # get content
    text = nobullets()

    # authenticate so that you can access the google doc
    service = _getservice(docID)

    # find end of current google doc content
    document = service.documents().get(documentId=docID).execute()
    doclines = document.get('body')['content']
    content = ""
    for line in doclines[1:]:
        content += line['paragraph']['elements'][0]['textRun']['content']
    startIndex = len(content)

    # paste the content onto the google doc
    payload = {
        "requests": [{"insertText": {"text": text, "endOfSegmentLocation": {"segmentId": ""}}}],
        "writeControl": {},
    }

    request = service.documents().batchUpdate(documentId=docID, body=payload)
    try:
        response = request.execute()
    except HttpError as e:
        print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

    # find end of current google doc content
    document = service.documents().get(documentId=docID).execute()
    doclines = document.get('body')['content']
    content = ""
    for line in doclines[1:]:
        content += line['paragraph']['elements'][0]['textRun']['content']
    endIndex = len(content)

    # make post request, turning pasted content into bulleted list
    payload = {
        "requests": [
            {
                "createParagraphBullets": {
                    "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                    "range": {"startIndex": startIndex + 1, "endIndex": endIndex, "segmentId": ""},
                }
            }
        ],
        "writeControl": {},
    }

    request = service.documents().batchUpdate(documentId=docID, body=payload)
    try:
        response = request.execute()  # noqa: F841
    except HttpError as e:
        print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

    # return
    return text


# HIDDEN FUNCTIONS


# Authorizes the user to access Google Docs
# CITATION: Google Docs API quickstart
def _getservice(DOCUMENT_ID, SCOPES=None):
    """Credentials testing

    Gets permissions to access the Google Docs API for a given Google Doc.

    Args:
        DOCUMENT_ID (str): The ID of a Google Doc.
        SCOPES (str): The permissions desired; optional, default None.

    Returns:
        service: Object used to access the Google Docs API.

    """

    creds = None

    if SCOPES is None:
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/documents']
    else:
        if os.path.exists('../token.json'):
            os.remove('../token.json')

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
        return

    return service
