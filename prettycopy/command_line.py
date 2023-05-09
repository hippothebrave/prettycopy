import prettycopy as pc
import typer
from typing import Optional

app = typer.Typer()


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
