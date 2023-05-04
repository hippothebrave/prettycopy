import pyperclip
import re
from googleapiclient.errors import HttpError

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import googleapiclient.discovery

import nltk
from nltk import tokenize
from nltk.corpus import words
from textblob import TextBlob
from spellchecker import SpellChecker

try:
    nltk.data.find('tokenizers/words')
except LookupError:
    nltk.download("words", quiet=True)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download("punkt", quiet=True)


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

    text = nonewlines(text).strip("• ")
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

    text = text.strip()
    if text[0] == '"' and text[-1] == '"':
        return smartcopy(text)

    text = '"' + smartcopy(text) + '"'
    pyperclip.copy(text)
    return text


def quote(end_punctuation=None, text=None):
    """Add quotes (and optional punctuation) around clipboard contents.

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

    text = text.strip()
    if text[0] == '"' and text[-1] == '"':
        return smartcopy(text)

    if end_punctuation is not None:
        if len(end_punctuation) != 1:
            raise ValueError("End punctuation should be a single character.")
        elif end_punctuation not in [',', '.', '!', '?']:
            raise ValueError("End punctuation should be one of: [.,!?]")
        text = '"' + smartcopy(text) + end_punctuation + '"'
    else:
        text = '"' + smartcopy(text) + '"'
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


def smartcopy(text=None):
    """Removes line breaks from clipboard contents in a smart way.

    Removes line breaks--adding a space if a line break splits a word in two, but not
    if the line break is between words--from a text input from the argument or (by default) the clipboard.

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

    text = trimspacing(text)
    lines = tokenize.sent_tokenize(text)
    for i in range(len(lines) - 1):
        start = text.find(lines[i]) + len(lines[i])  # char after end of sentence
        end = text.find(lines[i + 1])  # char @ beginning of next sentence
        lines[i] = _cleanlines(lines[i])
        substr = text[start:end]
        if '\n' in substr:
            lines[i] = lines[i] + '\n'
        else:
            lines[i] = lines[i] + ' '

    lines[-1] = _cleanlines(lines[-1])

    text = ''.join(lines)

    pyperclip.copy(text)
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


def _cleanlines(line):
    """
    Removes newlines from a given line, adding a space if it's surrounded by
    recognizable English words, and no space if it isn't.
    """
    spell = SpellChecker()
    # remove newlines "within words"
    for match in re.finditer(r"([A-Za-z0-9]+)(\r?\n)+([A-Za-z0-9]+)", line):
        b1 = TextBlob(match.group(1))
        b2 = TextBlob(match.group(3))

        loc = line.find(str(match.group(1) + match.group(2) + match.group(3))) + len(match.group(1))

        if (
            match.group(1) == spell.correction(match.group(1))
            or match.group(1) == b1.correct()
            or match.group(1) in words.words()
        ) and (
            match.group(3) == spell.correction(match.group(3))
            or match.group(3) == b2.correct()
            or match.group(3) in words.words()
        ):
            line = list(line)
            line[loc] = " "
            line = ''.join(line)
        else:
            line = list(line)
            line[loc] = ""
            line = ''.join(line)

    # remove any remaining newlines
    line = re.sub(r"(\r?\n)+", "", line)
    return line
