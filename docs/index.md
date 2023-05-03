```{toctree}
:hidden:

dev_intro.md
```

# Welcome to prettycopy's documentation!

Welcome to PrettyCopy: a beginner-friendly library intended to ensure clean, format-friendly copy-pasting!

[![License](https://img.shields.io/github/license/hippothebrave/prettycopy)](https://github.com/hippothebrave/prettycopy/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/hippothebrave/prettycopy)](https://github.com/hippothebrave/prettycopy/issues)
[![Build Status](https://github.com/hippothebrave/prettycopy/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/hippothebrave/prettycopy/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/hippothebrave/prettycopy/branch/main/graph/badge.svg)](https://codecov.io/gh/hippothebrave/prettycopy)
[![PyPI](https://img.shields.io/pypi/v/prettycopy)](https://pypi.org/project/prettycopy/)

## Overview
Copying and pasting text is one of the most commonly-used functionalities we have on our computers. But sometimes, there are formatting issues in the text you're copying that a simple Ctrl+V or Ctrl+Shift+V can't fix.

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
In the command line, type `prettycopy [function_name] [any_args]`. 
PrettyCopy will print the corrected text, just to show you what your clipboard current contains. 
Now, as soon as you paste, the text will already be corrected.

If you want, you can add the option `--text "your_text_here"` to the instruction. In this case, PrettyCopy will take your inputted string, correct it, and place it in the clipboard. Remember to add quotation marks around your input string if it contains whitespace. This option can go anywhere as long as the input string is to the right of the --text flag.

Confused? Type `prettycopy --help` to get a list of possible functions, and `prettycopy [function_name] --help` to get help for any particular function.

<img src="https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/pchelp.gif" alt= “Example usage of the code” width="25%" height="25%">

### In a Program
PrettyCopy will take in some text, correct it, and copy the corrected text to your clipboard. It will also return the corrected text as a return value, in case you want to keep using it (for example, in a nested function).
By default, PrettyCopy will run on the text in your clipboard. If you want to correct a different text, enter your preferred text as an argument.

## Functions

```{eval-rst}
.. autofunction:: prettycopy.prettycopy.bullettopar
```

EXAMPLE:
```python
import prettycopy.prettycopy as pc
# If you have copied the text:
    # • Example
    # • text
    # • here
pc.bullettopar()
# your clipboard content becomes: 
    # Example text here
```

<img src="https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/pcbullettopar.gif" alt= “Example usage of the code” width="25%" height="25%">


```{eval-rst}
.. autofunction:: prettycopy.prettycopy.nonewlines
```

EXAMPLE:
```python
import prettycopy.prettycopy as pc
# If you have copied the text:
    # Example
    # text
    # here
pc.nonewlines()
# your clipboard content becomes: 
    # Example text here
```

<img src="https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/pcnonewlines.gif" alt= “Example usage of the code” width="25%" height="25%">


```{eval-rst}
.. autofunction:: prettycopy.prettycopy.nobullets
```

EXAMPLE:
```python
import prettycopy.prettycopy as pc
# If you have copied the text:
    # • Example
    # • text
    # • here
pc.nobullets()
# your clipboard content becomes: 
    # Example 
    # text 
    # here
```

<img src="https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/pcnobullets.gif" alt= “Example usage of the code” width="25%" height="25%">


```{eval-rst}
.. autofunction:: prettycopy.prettycopy.simplequote
```

EXAMPLE:
```python
import prettycopy.prettycopy as pc
# If you have copied the text:
    # Example text here
pc.simplequote()
# your clipboard content becomes: 
    # "Example text here"
```


```{eval-rst}
.. autofunction:: prettycopy.prettycopy.quote
```

EXAMPLES:
```python
import prettycopy.prettycopy as pc
# If you have copied the text:
    # Example text here
pc.quote()
# your clipboard content becomes: 
    # "Example text here,"

# If you copy the same text:
    # Example text here
pc.quote('!')
# your clipboard content becomes: 
    # "Example text here!"
```


```{eval-rst}
.. autofunction:: prettycopy.prettycopy.trimspacing
```

EXAMPLES:
```python
import prettycopy.prettycopy as pc
# If you have copied the text:
    # Example 
    # 
    # text 
    # 
    # here
pc.trimspacing()
# your clipboard content becomes: 
    # Example
    # text 
    # here
```


```{eval-rst}
.. autofunction:: prettycopy.prettycopy.trimspacing
```

EXAMPLES:
```python
import prettycopy.prettycopy as pc
# If you have copied the text:
    # Example 
    # 
    # text 
    # 
    # here
pc.trimspacing()
# your clipboard content becomes: 
    # Example
    # text 
    # here
```


```{eval-rst}
.. autofunction:: prettycopy.prettycopy.smartcopy
```

EXAMPLES:
```python
import prettycopy.prettycopy as pc
# If you have copied the text:
    # Example sen
    # tence goes
    # here.
pc.smartcopy()
# your clipboard content becomes: 
    # Example sentence goes here.
```


```{eval-rst}
.. autofunction:: prettycopy.prettycopy.betterbullets
```

(Note: this function is still under development! *Do not use it. It will not work.*)

## For developers

Any interested developers, please head to [Intro for Developers](dev_intro.md).
