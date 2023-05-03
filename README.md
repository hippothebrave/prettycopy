# prettycopy
A beginner-friendly library for clean, format-friendly copy-pasting.

[![License](https://img.shields.io/github/license/hippothebrave/prettycopy)](https://github.com/hippothebrave/prettycopy/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/hippothebrave/prettycopy)](https://github.com/hippothebrave/prettycopy/issues)
[![Build Status](https://github.com/hippothebrave/prettycopy/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/hippothebrave/prettycopy/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/hippothebrave/prettycopy/branch/main/graph/badge.svg)](https://codecov.io/gh/hippothebrave/prettycopy)
[![PyPI](https://img.shields.io/pypi/v/prettycopy)](https://pypi.org/project/prettycopy/)
[![Documentation](https://img.shields.io/badge/Documentation-ReadTheDocs-informational)](https://prettycopy.readthedocs.io/en/latest/)

## Overview
Copying and pasting text is one of the most commonly-used functionalities we have on our computers. But sometimes, there are formatting issues in the text you're copying that a simple 'paste without formatting' can't fix.

Enter prettycopy.

PrettyCopy will help you clean up the text on your clipboard *before* you paste it. Just copy text, run a PrettyCopy function, and you'll be able to paste it with corrections already in place!

See our documentation [here](https://prettycopy.readthedocs.io/en/latest/).

### Installation

If you already have Python, just run:

```bash
pip install prettycopy
```

## Usage

So... how do you use PrettyCopy? It's very simple! You can use PrettyCopy at the command line, or through your own program.

### Command Line
Copy a piece of text.
In the command line, type `prettycopy [function_name] [any_args]`. 
PrettyCopy will print the corrected text, just to show you what your clipboard current contains. 
Now, as soon as you paste, the text will already be corrected.

If you want, you can add the option `--text "your_text_here"` to the instruction. In this case, PrettyCopy will take your inputted string, correct it, and place it in the clipboard. Remember to add quotation marks around your input string if it contains whitespace. This option can go anywhere as long as the input string is to the right of the --text flag.

Confused? Type `prettycopy --help` to get a list of possible functions, and `prettycopy [function_name] --help` to get help for any particular function.

### In a Program
PrettyCopy will take in some text, correct it, and copy the corrected text to your clipboard. It will also return the corrected text as a return value, in case you want to keep using it (for example, in a nested function).
By default, PrettyCopy will run on the text in your clipboard. If you want to correct a different text, enter your preferred text as an argument.

### Functions

`prettycopy.nonewlines(optional_text)`: Removes all line breaks from the text.

`prettycopy.nobullets(optional_text)`: Removes all bullet symbols (•) and replaces them with line breaks.

`prettycopy.bullettopar(optional_text)`: Removes all line breaks and bullet symbols (•) and replaces them with spaces, returning a single paragraph.

`prettycopy.simplequote(optional_text)`: Adds quotation marks around the text.

`prettycopy.quote(optional_end_punctuation, optional_text)`: Adds quotation marks around the text, ending in a punctuation mark. The default is a comma.

> Example: *this is a test* --> prettycopy.quote() --> *"this is a test,"*

> Example: *this is a test* --> prettycopy.quote('!') --> *"this is a test!"*

`prettycopy.trimspacing(optional_text)`: Removes empty lines.

`prettycopy.smartcopy(optional_text)`: Removes line breaks in an intelligent manner: adding spaces between words, but not inside words that have been split.

> Example: *this\nis a te\nst* --> prettycopy.smartcopy() --> *this is a test*

`prettycopy.betterbullets(docID)`: If you enter the document ID of an editable Google Doc (the long string of letters and numbers in the URL), this function will copy the text in your clipboard to the end of the document, replacing all bullet symbols (•) with correctly-formatted bullet points. Still under construction.
