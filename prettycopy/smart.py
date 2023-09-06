import pyperclip
import re
from googleapiclient.errors import HttpError

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import googleapiclient.discovery

import nltk
from nltk import tokenize
from nltk.corpus import words
from textblob import TextBlob

try:
    nltk.data.find('tokenizers/words')
except LookupError:
    nltk.download("words", quiet=True)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download("punkt", quiet=True)


