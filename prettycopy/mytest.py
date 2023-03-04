import pyperclip
import sys  # sys.argv[0] is mytest.py, etc
import re
import gdocs
from googleapiclient.errors import HttpError


def nonewlines():
    """Remove all newlines."""
    text = pyperclip.paste()
    text = ''.join(text.splitlines())
    pyperclip.copy(text)
    return text


def nobullets():
    """Take out old newlines, replace bullets with newlines."""
    text = pyperclip.paste()
    text = nonewlines().lstrip("• ")
    text = re.sub("•\s*", "\n", text)
    pyperclip.copy(text)
    return text


def bullettopar():
    """Remove newlines, replace bullets with spaces"""
    text = pyperclip.paste()
    text = ' '.join([re.sub("•\s*", " ", line).strip() for line in text.splitlines()])
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
        response = request.execute()
    except HttpError as e:
        print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

    # return
    return text


def quote(end_punctuation=False):
    """Add quotes (and optional comma) around clipboard contents."""
    if end_punctuation:
        text = '"' + pyperclip.paste() + ',"'
    else:
        text = '"' + pyperclip.paste() + '"'
    pyperclip.copy(text)
    return text


if __name__ == "__main__":
    match sys.argv[1]:
        case 'nonewlines':
            print(nonewlines())
        case 'nobullets':
            print(nobullets())
        case 'bullettopar':
            print(bullettopar())
        case 'betterbullets':
            print(betterbullets(sys.argv[2]))
        case 'quote':
            print(quote(True))
        case 'endquote':
            print(quote())
    print("You did it!")
