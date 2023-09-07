import prettycopy as pc
from . import basics
import pyperclip
import typer
from typing import Optional, Tuple
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def copy(
    text: str = "",
    output: bool = True,
    no_gaps: bool = False,
    no_linebreaks: bool = False,
    no_bullets: bool = False,
    quote: bool = False,
    end_punct: str = "",
    line_punct: str = "",
    bullet_punct: str = "",
    replace: Annotated[Tuple[str, str], typer.Option()] = (None, None),
    remove: str = "",
    case: str = "",
):
    """
    Alter the contents of a copied text in the clipboard.

    The input comes from either an argument or (by default) the clipboard.

    Args:
        --text "YOUR_STRING": Use a given text instead of the clipboard contents.

        --no-output: Prevents the result from being printed to the command line.

        --no-gaps: Removes any blank lines.

        --no-linebreaks: Removes all line breaks from the text.

        --no-bullets: Removes line breaks, and replaces bullet points with line breaks.

        --quote: Adds quotation marks to the beginning and end of the text.

        --end-punct "PUNCTUATION_MARK": Adds a given punctuation mark to the end of the text.
        If the text is surrounded by quotation marks (' or "), the punctuation mark goes on the inside.
        Often combined with --quote.

        --line-punct "PUNCTUATION_MARK": Replaces all line breaks with a given punctuation mark.

        --bullet-punct "PUNCTUATION_MARK": Replaces all bullet points with a given punctuation mark.

        --replace "TO_BE_REPLACED" "TO_REPLACE": Replaces all instances of the first substring
        with the second.

        --remove "SUBSTRING": Removes all instances of the given substring.

        --case ["lower"/"upper"/"title"/"capital"]: Changes the text's case to lowercase; uppercase;
        title case; or capitalizes the first letter of every sentence.

    Returns:
        str: Corrected text.

    Warning:
        Changes contents of the clipboard.
    """
    try:
        # set up return value "ret"
        if text:
            ret = text
        else:
            ret = pyperclip.paste()

        # line gaps
        if no_gaps:
            ret = basics.nogaps(ret)

        # line breaks
        if no_linebreaks and not no_bullets:
            ret = basics.nolinebreaks(ret)
        elif not no_linebreaks and no_bullets:
            ret = basics.nobullets(ret)
        elif no_linebreaks and no_bullets:
            ret = basics.par(ret)

        # additions
        if end_punct:
            ret = basics.endpunct(end_punct, ret)
        if line_punct:
            ret = basics.punct(line_punct, bullets=False, text=ret)
        if bullet_punct:
            ret = basics.punct(bullet_punct, bullets=True, text=ret)
        if quote:
            ret = basics.quote(ret)

        # alterations
        if replace != (None, None):
            ret = basics.replace(replace[0], replace[1], text=ret)
        if remove:
            ret = basics.replace(remove, '', text=ret)
        if case:
            ret = basics.case(case, text=ret)

        # output
        if output:
            print(ret)
        pyperclip.copy(ret)
        return ret
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def nonewlines(text: str = "", output: bool = True):
    """
    Remove all lines breaks.
    From the clipboard, or, optionally, --text.
    """
    try:
        if text:
            ret = pc.nonewlines(text)
        else:
            ret = pc.nonewlines()
        if output:
            print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def bullettolist(text: str = "", output: bool = True):
    """
    Remove all line breaks and bullet points.
    From clipboard, or, optionally, --text.
    """
    try:
        if text:
            ret = pc.bullettolist(text)
        else:
            ret = pc.bullettolist()
        if output:
            print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def bullettopar(text: str = "", output: bool = True):
    """
    Turn text into a paragraph.
    From clipboard or, optionally, --text.
    """
    try:
        if text:
            ret = pc.bullettopar(text)
        else:
            ret = pc.bullettopar()
        if output:
            print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def simplequote(text: str = "", output: bool = True):
    """
    Add quotation marks around text.
    From clipboard or, optionally, --text.
    """
    try:
        if text:
            ret = pc.simplequote(text)
        else:
            ret = pc.simplequote()
        if output:
            print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def quote(end_punctuation: Optional[str] = typer.Argument(None), text: str = "", output: bool = True):
    """
    Add quotation marks and punctuation (default comma) to text. Clipboard or optional --text.
    """
    if end_punctuation and text:
        ret = pc.quote(end_punctuation=end_punctuation, text=text)
    elif end_punctuation and not text:
        ret = pc.quote(end_punctuation=end_punctuation)
    elif text and not end_punctuation:
        ret = pc.quote(text=text)
    else:
        ret = pc.quote()
    if output:
        print(ret)


@app.command()
def trimspacing(text: str = "", output: bool = True):
    """
    Remove empty lines.
    From clipboard or, optionally, --text.
    """
    try:
        if text:
            ret = pc.trimspacing(text)
        else:
            ret = pc.trimspacing()
        if output:
            print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def smartcopy(text: str = "", output: bool = True):
    """
    Remove line breaks in a "smart" manner, preventing words from being split.
    From clipboard or, optionally, --text.
    """
    try:
        if text:
            ret = pc.smartcopy(text)
        else:
            ret = pc.smartcopy()
        if output:
            print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def remove(substring: str, replacement: str = "", text: str = "", output: bool = True):
    """
    Remove all instances of a substring.
    From the clipboard, or, optionally, --text.
    """
    try:
        if text and replacement:
            ret = pc.remove(substring, replacement, text)
        elif text and not replacement:
            ret = pc.remove(substring, text=text)
        elif replacement and not text:
            ret = pc.remove(substring, replacement=replacement)
        else:
            ret = pc.remove(substring)
        if output:
            print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))
