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

### Usage

Copy a piece of text. Run a PrettyCopy function. Now, when you paste, the text will already by corrected. That's all!

For added flexibility:

You can enter the text as an argument to the function, and PrettyCopy will automatically copy the corrected text to your clipboard. Plus, if you're using PrettyCopy functions through code, the functions return the corrected text as a string.

### Functions

`prettycopy.nonewlines(optional_text)`: Removes all line breaks from the text.

`prettycopy.nobullets(optional_text)`: Removes all bullet symbols (•) and replaces them with line breaks.

`prettycopy.bullettopar(optional_text)`: Removes all line breaks and bullet symbols (•) and replaces them with spaces, returning a single paragraph.

`prettycopy.simplequote(optional_text)`: Adds quotation marks around the text.

`prettycopy.quote(optional_end_punctuation, optional_text)`: Adds quotation marks around the text, ending in a punctuation mark. The default is a comma.

> Example: *this is a test* --> prettycopy.quote() --> *"this is a test,"*

> Example: *this is a test* --> prettycopy.quote('!') --> *"this is a test!"*

`prettycopy.betterbullets(docID)`: If you enter the document ID of an editable Google Doc (the long string of letters and numbers in the URL), this function will copy the text in your clipboard to the end of the document, replacing all bullet symbols (•) with correctly-formatted bullet points. Still under construction.
