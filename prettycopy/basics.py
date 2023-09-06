import pyperclip
import re
import string
from nltk.tokenize import sent_tokenize


# HELPER
def _gettext(text):
    if text is None:
        text = pyperclip.paste()
    if not isinstance(text, str):
        raise ValueError("PrettyCopy can only take in strings!")
    return text


# REMOVING LINE BREAKS


def nolinebreaks(text=None):
    """Remove all line breaks.

    Args:
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.

    """
    text = _gettext(text)

    text = ' '.join([line.strip() for line in text.split()])
    pyperclip.copy(text)
    return text


def nobullets(text=None):
    """Take out old line breaks. Replace bullets with line breaks.

    Args:
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.

    """
    text = _gettext(text)

    text = nolinebreaks(text).strip("• ")
    text = re.sub(r"\s*•\s*", "\n", text)
    pyperclip.copy(text)
    return text


def par(text=None):
    """Remove newlines, replace bullets with spaces.

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


# ADD


def quote(text=None):
    """Add quotes around clipboard contents if none exist.

    Args:
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.

    """
    text = _gettext(text)

    text = text.strip()
    if text[0] == '"' and text[-1] == '"':
        return text

    text = '"' + text + '"'
    pyperclip.copy(text)
    return text


# TODO: decide what to do w/r/t quotation marks, parentheses, etc.
def endpunct(end_punct, text=None):
    """Add a final punctuation mark to the contents.

    If it ends with a quotation mark, punctuation goes inside the quotation mark.

    Args:
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard."""

    text = _gettext(text)

    text = text.strip()

    if len(end_punct) != 1:
        raise ValueError("End punctuation should be a single character.")
    elif end_punct not in string.punctuation:
        raise ValueError("End punctuation should be one of: " + string.punctuation)

    if text[-1] in ['"', "'"]:
        text = text[:-1] + end_punct + text[-1]
    else:
        text = text + end_punct

    pyperclip.copy(text)
    return text


def punct(punct, bullets=False, text=None):
    """Add a punctuation between every line break OR instead of bullet points.

    Args:
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard."""

    text = _gettext(text)

    if len(punct) != 1:
        raise ValueError("End punctuation should be a single character.")
    elif punct not in string.punctuation:
        raise ValueError("Punctuation should be one of: " + string.punctuation)

    if bullets:
        text = nobullets(text)

    text = (punct + ' ').join([line.strip() for line in text.splitlines()])

    pyperclip.copy(text)
    return text


# GAPS


def nogaps(text=None):
    """Removes empty lines.

    Args:
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.
    """
    text = _gettext(text)

    text = re.sub(r"(\r?\n)+", "\n", text)
    text = text.strip()
    pyperclip.copy(text)
    return text


# ALTER


def replace(substring, replacement=None, text=None):
    """Remove or replace a substring.

    Args:
        substring (str): A string to be removed or replaced.
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.

    """

    text = _gettext(text)

    if replacement:
        text = text.replace(substring, replacement)
    else:
        text = text.replace(substring, '')

    pyperclip.copy(text)
    return text


def case(case=None, text=None):
    """Alter the case of a text.

    Args:
        case (str): What case to change the text to.
        "lower" for lowercase; "upper" for uppercase; "title" for title case; "capital" to capitalize first words
        text (str): Any text; optional, default None.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.

    """

    text = _gettext(text)

    if case not in ["lower", "upper", "title", "capital"]:
        return ValueError("Case must be one of ['lower', 'upper', 'title', 'capital'].")

    if case == "lower":
        text = text.lower()
    elif case == "upper":
        text = text.upper()
    elif case == "title":
        text = text.title()
    elif case == "capital":
        text = ' '.join(line.capitalize() for line in sent_tokenize(text))

    pyperclip.copy(text)
    return text
