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

Copy a piece of text. Run a PrettyCopy function. Now, when you paste, the text will already be corrected. That's all!



For added flexibility: You can enter the text as an argument to the function, and PrettyCopy will automatically copy the corrected text to your clipboard. Plus, if you're using PrettyCopy functions through code, the functions return the corrected text as a string.

## Functions

<!-- ```{eval-rst}
.. automodule:: prettycopy.prettycopy
   :members:
``` -->

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

<img src="https://raw.githubusercontent.com/hippothebrave/prettycopy/main/docs/images/bullettopar.gif" alt= “Example usage of the code” width="25%" height="25%">


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
