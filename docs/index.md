```{toctree}
:hidden:

dev_intro.md
```

# Welcome to PrettyCopy's documentation!

Welcome to PrettyCopy: a beginner-friendly library intended to ensure clean, format-friendly copy-pasting!

[![License](https://img.shields.io/github/license/hippothebrave/prettycopy)](https://github.com/hippothebrave/prettycopy/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/hippothebrave/prettycopy)](https://github.com/hippothebrave/prettycopy/issues)
[![Build Status](https://github.com/hippothebrave/prettycopy/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/hippothebrave/prettycopy/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/hippothebrave/prettycopy/branch/main/graph/badge.svg)](https://codecov.io/gh/hippothebrave/prettycopy)
[![PyPI](https://img.shields.io/pypi/v/prettycopy)](https://pypi.org/project/prettycopy/)
[![Documentation Status](https://readthedocs.org/projects/prettycopy/badge/?version=latest)](https://prettycopy.readthedocs.io/en/latest/?badge=latest)

## Overview
Everybody copies and pastes text. But sometimes, you want to change something about the text you just copied. Maybe the text has a line break in the middle of every sentence; maybe there's an extra empty space between every line; maybe you want to change it all into upper case, or add quotes around it, or--

Enter PrettyCopy.

PrettyCopy will help you clean up the text on your clipboard *before* you paste it. Just copy text, run a PrettyCopy function, and you'll be able to paste it with corrections *already in place*!

## Installation

If you already have Python, just run:

```python
pip install prettycopy
```

## Usage

So... how do you use PrettyCopy? It's very simple! You can use PrettyCopy at the command line, or through your own program.

### Command Line
Copy a piece of text.

In the command line, type `prettycopy [function_name] [any_args] [any_flags]`. 

PrettyCopy will print the (corrected) contents of your clipboard.

When you paste, the text will already be corrected!

#### Command Line Function

PrettyCopy has a main command-line function: `copy`. The `copy` function can potentially take in a wide variety of optional flags, which allows it to use and combine the abilities of the other PrettyCopy functions.

```{eval-rst}
.. autofunction:: prettycopy.command_line.copy
```

#### Other Functions

All functions have some optional flags.

`--no-output` will prevent PrettyCopy from copying your clipboard contents to the terminal. (Useful for long inputs.)

`--text "your_text_here"` allows you to use a command-line string (to the right of the flag, encased in quotation marks) instead of your current clipboard contents. Note that *your clipboard contents will still be replaced*! 

#### Help

Confused? Type `prettycopy --help` to get a list of possible functions, and `prettycopy [function_name] --help` to get help for any particular function.

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/pchelp.gif
    :width: 700
    :align: center
```

### In a Program
Each PrettyCopy function takes in a string, corrects it, and copies the corrected text to your clipboard. It will also return the corrected text as a return value, in case you want to keep using it (for example, in a nested function).

By default, PrettyCopy will run on the text in your clipboard. If you want to correct a different text, enter your preferred text as an argument.

## Functions

### Smart Copy-and-Paste

When copying and pasting between formats, line breaks can appear between, or even within, ordinary words. The `smartcopy` function can for the most part distinguish between them, allowing your copy-and-paste experience to be as smooth as possible.

```{eval-rst}
.. autofunction:: prettycopy.smartcopy
```

EXAMPLES:

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/smartcopy_pc.gif
    :width: 700
    :align: center
```

```python
import prettycopy
# If you have copied the text:
    # Example sen
    # tence goes
    # here.
prettycopy.smartcopy()
# your clipboard content becomes: 
    # Example sentence goes here.
```

### Bullet-Point Cleaning

Sometimes you want to copy a piece of text with bullet points. This doesn't always work the way you'd like it to.

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/bullets_nopc.gif
    :width: 700
    :align: center
```

Using PrettyCopy, you can turn the text into a clean list, or into a single paragraph.

```{eval-rst}
.. autofunction:: prettycopy.bullettolist
```

EXAMPLES:

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/bullettolist_pc.gif
    :width: 700
    :align: center
```

```python
import prettycopy
# If you have copied the text:
    # • Example
    # • text
    # • here
prettycopy.bullettolist()
# your clipboard content becomes: 
    # Example 
    # text 
    # here
```



```{eval-rst}
.. autofunction:: prettycopy.bullettopar
```

EXAMPLES:

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/bullettopar_pc.gif
    :width: 700
    :align: center
```

```python
import prettycopy
# If you have copied the text:
    # • Example
    # • text
    # • here
prettycopy.bullettopar()
# your clipboard content becomes: 
    # Example text here
```


### Line Break Cleaning

Line breaks also don't always copy over right.

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/trimspace_nopc.gif
    :width: 700
    :align: center
```

PrettyCopy has functions to fix that!


```{eval-rst}
.. autofunction:: prettycopy.nonewlines
```

EXAMPLES:

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/pcnonewlines.gif
    :width: 700
    :align: center
```

```python
import prettycopy
# If you have copied the text:
    # Example
    # text
    # here
prettycopy.nonewlines()
# your clipboard content becomes: 
    # Example text here
```


```{eval-rst}
.. autofunction:: prettycopy.trimspacing
```

EXAMPLES:

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/trimspacing_pc.gif
    :width: 700
    :align: center
```

```python
import prettycopy
# If you have copied the text:
    # Example 
    # 
    # text 
    # 
    # here
prettycopy.trimspacing()
# your clipboard content becomes: 
    # Example
    # text 
    # here
```


### Copying Quotes

Ever wanted to copy a quote from a document?

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/quotes_nopc.gif
    :width: 700
    :align: center
```

PrettyCopy can help!


```{eval-rst}
.. autofunction:: prettycopy.simplequote
```

EXAMPLES:

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/simplequote_pc.gif
    :width: 700
    :align: center
```

```python
import prettycopy
# If you have copied the text:
    # Example text here
prettycopy.simplequote()
# your clipboard content becomes: 
    # "Example text here"
```



```{eval-rst}
.. autofunction:: prettycopy.quote
```

EXAMPLES:

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/quote_pc.gif
    :width: 700
    :align: center
```

```python
import prettycopy
# If you have copied the text:
    # Example text here
prettycopy.quote()
# your clipboard content becomes: 
    # "Example text here,"

# If you copy the same text:
    # Example text here
prettycopy.quote('!')
# your clipboard content becomes: 
    # "Example text here!"
```
### Miscellaneous 

There are other ways that you might want to edit the text that you copied before pasting it. PrettyCopy can help you here, too!

```{eval-rst}
.. autofunction:: prettycopy.remove
```

EXAMPLES:

```{eval-rst}
.. image:: https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/remove_pc.gif
    :width: 700
    :align: center
```

```python
import prettycopy
# If you have copied the text:
    # Example text here
prettycopy.remove('ex')
# your clipboard content becomes: 
    # Example tt here
```

### Integrations

(Note: this function is still under development! *Do not use it. It will not work.*)

```{eval-rst}
.. autofunction:: prettycopy.betterbullets
```

## For developers

Any interested developers, please head to [Intro for Developers](dev_intro.md).
