import pyperclip
import re
import prettycopy.gdocs
from googleapiclient.errors import HttpError


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
    text = ''.join(text.splitlines())
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
    text = nonewlines().lstrip("• ")
    text = re.sub(r"•\s*", "\n", text)
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
    text = ' '.join([re.sub(r"•\s*", " ", line).strip() for line in text.splitlines()])
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
    service = prettycopy.gdocs.getservice()

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
