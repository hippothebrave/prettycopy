import pyperclip
import re
import gdocs
from googleapiclient.errors import HttpError


def nonewlines(text=None):
    """Remove all newlines."""
    if text is None:
        text = pyperclip.paste()
    text = ''.join(text.splitlines())
    pyperclip.copy(text)
    return text


def nobullets(text=None):
    """Take out old newlines, replace bullets with newlines."""
    if text is None:
        text = pyperclip.paste()
    text = nonewlines().lstrip("• ")
    text = re.sub(r"•\s*", "\n", text)
    pyperclip.copy(text)
    return text


def bullettopar(text=None):
    """Remove newlines, replace bullets with spaces"""
    if text is None:
        text = pyperclip.paste()
    text = ' '.join([re.sub(r"•\s*", " ", line).strip() for line in text.splitlines()])
    pyperclip.copy(text)
    return text


# FIXME: only works if you have the document ID
# FIXME: only pastes at end of document
def betterbullets(docID):
    """Add clipboard comment to end of Google Doc as a bulleted list."""
    # get content
    text = nobullets()

    # authenticate so that you can access the google doc
    service = gdocs.getservice()

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


def simplequote(text=None):
    """Add quotes around clipboard contents."""
    if text is None:
        text = pyperclip.paste()
    text = '"' + text + '"'
    pyperclip.copy(text)
    return text


def quote(end_punctuation=None, text=None):
    """Add quotes (and optional comma) around clipboard contents."""
    if text is None:
        text = pyperclip.paste()
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


# TODO: turn excess newlines into only one
