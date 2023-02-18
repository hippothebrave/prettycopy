import pyperclip
import sys #sys.argv[0] is mytest.py, etc
import re
import requests
import gdocs
from googleapiclient.errors import HttpError

# testing function
def tester():
    text = pyperclip.paste()
    text = "The text:" + text.upper()
    pyperclip.copy(text)
    return text

# remove all newlines
def nonewlines():
    text = pyperclip.paste()
    text = ''.join(text.splitlines())
    pyperclip.copy(text)
    return text

# take out old newlines; replace bullets with newlines
def nobullets():
    text = pyperclip.paste()
    text = ''.join([line.lstrip() for line in text.splitlines()])
    text = re.sub("•\s*", "\n", text)
    pyperclip.copy(text)
    return text

# remove newlines, replace bullets with spaces
def bullettopar():
    text = pyperclip.paste()
    text = ' '.join([re.sub("•\s*", " ", line).strip() for line in text.splitlines()])
    pyperclip.copy(text)
    return text

# remove bullet symbols, turn into bulleted list
# FIXME: only works if you have the document ID
def betterbullets(docID):
    # get content
    text = "\n" + nobullets()

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
        "requests": [
            {
            "insertText": {
                "text": text,
                "endOfSegmentLocation": {
                "segmentId": ""
                }
            }
            }
        ],
        "writeControl": {}
    }

    request = service.documents().batchUpdate(documentId = docID, body=payload)
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
                "range": {
                    "startIndex": startIndex + 1,
                    "endIndex": endIndex,
                    "segmentId": ""
                }
            }
            }
        ],
        "writeControl": {}
    }

    request = service.documents().batchUpdate(documentId = docID, body=payload)
    try:
        response = request.execute()
    except HttpError as e:
        print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

    # return
    return text

def quote(end_punctuation=False):
    if(end_punctuation):
        text = '"' + pyperclip.paste() + ',"'
    else:
        text = '"' + pyperclip.paste() + '"'
    pyperclip.copy(text)
    return text

if __name__ == "__main__":
    match sys.argv[1]:
        case 'test':
            print(tester())
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
