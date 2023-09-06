# prettycopy
A beginner-friendly library for clean, format-friendly copy-pasting.

[![License](https://img.shields.io/github/license/hippothebrave/prettycopy)](https://github.com/hippothebrave/prettycopy/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/hippothebrave/prettycopy)](https://github.com/hippothebrave/prettycopy/issues)
[![Build Status](https://github.com/hippothebrave/prettycopy/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/hippothebrave/prettycopy/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/hippothebrave/prettycopy/branch/main/graph/badge.svg)](https://codecov.io/gh/hippothebrave/prettycopy)
[![PyPI](https://img.shields.io/pypi/v/prettycopy)](https://pypi.org/project/prettycopy/)
[![Documentation Status](https://readthedocs.org/projects/prettycopy/badge/?version=latest)](https://prettycopy.readthedocs.io/en/latest/?badge=latest)

## Overview
Copying and pasting text is one of the most commonly-used functionalities we have on our computers. But sometimes, there are formatting issues in the text you're copying that a simple 'paste without formatting' can't fix.

Enter PrettyCopy.

PrettyCopy will help you clean up the text on your clipboard *before* you paste it. Just copy your text, run a PrettyCopy function, and you'll be able to paste it with corrections already in place!

See our documentation [here](https://prettycopy.readthedocs.io/en/latest/).

### Installation

If you already have Python, just run:

```bash
pip install prettycopy
```

## Usage

So... how do you use PrettyCopy? It's very simple! You can use PrettyCopy functions at the command line, or through your own program.

Learn more about the functions using `prettycopy --help` at the command line, or by checking our [documentation](https://prettycopy.readthedocs.io/en/latest/).

### Command Line
Copy a piece of text.
In the command line, type `prettycopy [function_name] [any_args]`. 
PrettyCopy will print the corrected text, just to show you what your clipboard current contains. 
Now, as soon as you paste, the text will already be corrected.

All command-line functions have the `--text [YOUR_STRING]` flag. PrettyCopy will take your inputted string, correct it, and place it in the clipboard. *Remember to add quotation marks around your input string if it contains whitespace!* This option can go anywhere as long as the input string is to the right of the --text flag.

Confused? Type `prettycopy --help` to get a list of possible functions, and `prettycopy [function_name] --help` to get help for any particular function.

### In a Program
PrettyCopy will take in some text, correct it, and copy the corrected text to your clipboard. It will also return the corrected text as a return value, in case you want to keep using it (for example, in a nested function).
By default, PrettyCopy will run on the text in your clipboard. If you want to correct a different text, enter your preferred text as an argument.

## Examples
PrettyCopy can be used for fixing issues with line breaks; removing extraneous bullet point symbols; adding quotation marks (and optional punctuation) around a copied text; and more! 

![](https://github.com/hippothebrave/prettycopy/blob/main/docs/images/smartcopy_pc.gif)

See the [documentation](https://prettycopy.readthedocs.io/en/latest/) for the complete list of functions.

