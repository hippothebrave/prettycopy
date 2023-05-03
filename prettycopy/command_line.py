import prettycopy as pc
import typer
from typing import Optional

app = typer.Typer()


@app.command()
def nonewlines(text: str = ""):
    """
    Remove all lines breaks.
    From the clipboard, or, optionally, --text.
    """
    try:
        if text:
            ret = pc.nonewlines(text)
        else:
            ret = pc.nonewlines()
        print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def nobullets(text: str = ""):
    """
    Remove all line breaks and bullet points.
    From clipboard, or, optionally, --text.
    """
    try:
        if text:
            ret = pc.nobullets(text)
        else:
            ret = pc.nobullets()
        print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def bullettopar(text: str = ""):
    """
    Turn text into a paragraph.
    From clipboard or, optionally, --text.
    """
    try:
        if text:
            ret = pc.bullettopar(text)
        else:
            ret = pc.bullettopar()
        print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def simplequote(text: str = ""):
    """
    Add quotation marks around text.
    From clipboard or, optionally, --text.
    """
    try:
        if text:
            ret = pc.simplequote(text)
        else:
            ret = pc.simplequote()
        print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def quote(end_punctuation: Optional[str] = typer.Argument(None), text: str = ""):
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
    print(ret)


@app.command()
def trimspacing(text: str = ""):
    """
    Remove empty lines.
    From clipboard or, optionally, --text.
    """
    try:
        if text:
            ret = pc.trimspacing(text)
        else:
            ret = pc.trimspacing()
        print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def smartcopy(text: str = ""):
    """
    Remove line breaks in a "smart" manner, preventing words from being split.
    From clipboard or, optionally, --text.
    """
    try:
        if text:
            ret = pc.smartcopy(text)
        else:
            ret = pc.smartcopy()
        print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))


@app.command()
def nonewlinequote(text: str = ""):
    """
    Removes line breaks from a text, and adds quotation marks around it.
    From clipboard or, optionally, --text.
    """
    try:
        if text:
            ret = pc.simplequote(pc.nonewlines(text))
        else:
            ret = pc.simplequote(pc.nonewlines())
        print(ret)
    except ValueError:
        print(typer.style("Input should have been a string!", fg="white", bg="red"))
