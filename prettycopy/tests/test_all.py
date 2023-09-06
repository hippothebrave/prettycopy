import prettycopy.prettycopy as pc
from prettycopy.command_line import app

from unittest.mock import patch, MagicMock
from googleapiclient.errors import HttpError
from typer.testing import CliRunner
import typer

import pytest

# TEST
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download("punkt", quiet=True)
# \TEST


runner = CliRunner()


def test_nonewlines():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        # Bad type
        paste_mock.return_value = 77
        with pytest.raises(ValueError):
            ret = pc.nonewlines()

        # Text from clipboard
        paste_mock.return_value = "Testing\n line \nof text\n here."
        ret = pc.nonewlines()
        assert ret == "Testing line of text here."
        assert copy_mock.call_args.args == (ret,)

        # Spacing
        paste_mock.return_value = "Testing\nline\nof text\nhere."
        ret = pc.nonewlines()
        assert ret == "Testing line of text here."
        assert copy_mock.call_args.args == (ret,)

        # Text from argument
        ret = pc.nonewlines("Another\n line \nof text\n here.")
        assert ret == "Another line of text here."
        assert copy_mock.call_args.args == (ret,)


def test_bullettolist():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock, patch(
        "prettycopy.prettycopy.nonewlines"
    ) as newline_mock:
        # Bad type
        paste_mock.return_value = 42
        with pytest.raises(ValueError):
            ret = pc.bullettolist()

        # No spaces
        paste_mock.return_value = "•Test\n•Test"
        newline_mock.return_value = '•Test •Test'
        ret = pc.bullettolist()
        assert newline_mock.call_args.args == ("•Test\n•Test",)
        assert ret == "Test\nTest"
        assert copy_mock.call_args.args == (ret,)

        # Spaces between bullet and text
        paste_mock.return_value = "• Test\n• Test"
        newline_mock.return_value = '• Test • Test'
        ret = pc.bullettolist()
        assert newline_mock.call_args.args == ("• Test\n• Test",)
        assert ret == "Test\nTest"
        assert copy_mock.call_args.args == (ret,)

        # Spaces around bullet and text
        paste_mock.return_value = "   • Test\n  •\tTest   •"
        newline_mock.return_value = '• Test • Test •'
        ret = pc.bullettolist()
        assert newline_mock.call_args.args == ("   • Test\n  •\tTest   •",)
        assert ret == "Test\nTest"
        assert copy_mock.call_args.args == (ret,)

        # Bullets within words
        paste_mock.return_value = "•   Te•st• Test"
        newline_mock.return_value = '• Te•st• Test'
        ret = pc.bullettolist()
        assert newline_mock.call_args.args == ("•   Te•st• Test",)
        assert ret == "Te\nst\nTest"
        assert copy_mock.call_args.args == (ret,)

        # Text from argument
        newline_mock.return_value = '•Another •Test'
        ret = pc.bullettolist("•Another\n•Test")
        assert newline_mock.call_args.args == ("•Another\n•Test",)
        assert ret == "Another\nTest"
        assert copy_mock.call_args.args == (ret,)


def test_bullettopar():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        # Bad type
        paste_mock.return_value = 77
        with pytest.raises(ValueError):
            pc.bullettopar()

        # No spaces
        paste_mock.return_value = "•Test\n•Test"
        ret1 = pc.bullettopar()
        assert ret1 == "Test Test"
        assert copy_mock.call_args.args == (ret1,)

        # Spaces after bullets
        paste_mock.return_value = "• Test\n• Test"
        ret2 = pc.bullettopar()
        assert ret2 == "Test Test"
        assert copy_mock.call_args.args == (ret2,)

        # Spaces around bullet and text
        paste_mock.return_value = "   • Test\n  •\tTest   •"
        ret3 = pc.bullettopar()
        assert ret3 == "Test Test"
        assert copy_mock.call_args.args == (ret3,)

        # Bullets within words
        paste_mock.return_value = "•   Te•st• Test"
        ret4 = pc.bullettopar()
        assert ret4 == "Te st Test"
        assert copy_mock.call_args.args == (ret4,)

        # Text from argument
        ret5 = pc.bullettopar("•Another\n•Test")
        assert ret5 == "Another Test"
        assert copy_mock.call_args.args == (ret5,)


def test_simplequote():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock, patch(
        "prettycopy.smartcopy"
    ) as smartcopy_mock:
        # Bad type
        paste_mock.return_value = 77
        with pytest.raises(ValueError):
            ret = pc.simplequote()

        # Already has quotes
        paste_mock.return_value = '"Test test"'
        smartcopy_mock.return_value = '"Test test"'
        ret = pc.simplequote()
        assert ret == '"Test test"'
        assert copy_mock.call_args.args == (ret,)

        # Argument from clipboard
        paste_mock.return_value = 'Test test'
        smartcopy_mock.return_value = 'Test test'
        ret = pc.simplequote()
        assert ret == '"Test test"'
        assert copy_mock.call_args.args == (ret,)

        # Text from argument
        smartcopy_mock.return_value = 'Another test'
        ret = pc.simplequote('Another test')
        assert ret == '"Another test"'
        assert copy_mock.call_args.args == (ret,)


def test_quote():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock, patch(
        "prettycopy.smartcopy"
    ) as smartcopy_mock:
        # Bad type
        paste_mock.return_value = 77
        with pytest.raises(ValueError):
            ret = pc.quote()

        # Already has quotes
        paste_mock.return_value = '"Test test"'
        smartcopy_mock.return_value = '"Test test"'
        ret = pc.quote()
        assert ret == '"Test test"'
        assert copy_mock.call_args.args == (ret,)

        # No arguments
        paste_mock.return_value = 'Test test'
        smartcopy_mock.return_value = 'Test test'
        ret = pc.quote()
        assert ret == '"Test test"'
        assert copy_mock.call_args.args == (ret,)

        # Punctuation argument
        paste_mock.return_value = 'Test test'
        smartcopy_mock.return_value = 'Test test'
        ret = pc.quote('.')
        assert ret == '"Test test."'
        assert copy_mock.call_args.args == (ret,)

        # Text argument
        smartcopy_mock.return_value = 'Another test'
        ret = pc.quote(text='Another test')
        assert ret == '"Another test"'
        assert copy_mock.call_args.args == (ret,)

        # Text and punctuation argument
        smartcopy_mock.return_value = 'Another test'
        ret = pc.quote('!', 'Another test')
        assert ret == '"Another test!"'
        assert copy_mock.call_args.args == (ret,)

        # Incorrect punctuation argument
        paste_mock.return_value = 'Test test'
        smartcopy_mock.return_value = 'Test test'
        with pytest.raises(ValueError):
            ret = pc.quote('test')
        assert len('test') > 1

        # Incorrect punctuation argument
        paste_mock.return_value = 'Test test'
        smartcopy_mock.return_value = 'Test test'
        with pytest.raises(ValueError):
            ret = pc.quote(';')
        assert ';' not in [',', '.', '!', '?']


def test_trimspacing():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        # Bad type
        paste_mock.return_value = 77
        with pytest.raises(ValueError):
            ret = pc.trimspacing()

        # multi-line break
        paste_mock.return_value = "Test\n\n\nhere"
        ret = pc.trimspacing()
        assert ret == "Test\nhere"
        assert copy_mock.call_args.args == (ret,)

        # windows
        paste_mock.return_value = "Test\r\n\r\nhere"
        ret = pc.trimspacing()
        assert ret == "Test\nhere"
        assert copy_mock.call_args.args == (ret,)

        # no repeats, spacing at beginning or end
        paste_mock.return_value = "   Test\nhere\n"
        ret = pc.trimspacing()
        assert ret == "Test\nhere"
        assert copy_mock.call_args.args == (ret,)

        # text from argument
        ret = pc.trimspacing("Another\r\n\r\n\r\ntest")
        assert ret == "Another\ntest"
        assert copy_mock.call_args.args == (ret,)


def test_getservice():
    with patch("os.path.exists") as os_mock, patch(
        "google.oauth2.credentials.Credentials.from_authorized_user_file"
    ) as creds_file_mock, patch(
        "google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file"
    ) as get_secrets_mock, patch(
        "builtins.open"
    ) as open_mock, patch(
        "googleapiclient.discovery.build"
    ) as build_mock, patch(
        "builtins.print"
    ) as print_mock, patch(
        "os.remove"
    ) as os_remove_mock:
        SCOPES = ['https://www.googleapis.com/auth/documents']

        # Test 1: credentials do exist
        # check + get creds
        os_mock.return_value = True
        os_mock.call_count = 0
        fakecreds1 = MagicMock()
        fakecreds1.valid = True
        creds_file_mock.return_value = fakecreds1
        # build service
        fakeservice1 = MagicMock()
        build_mock.return_value = fakeservice1

        ret = pc._getservice('1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0')

        assert os_mock.call_count == 1
        assert creds_file_mock.call_count == 1
        assert build_mock.call_args.args == (
            'docs',
            'v1',
        )
        assert build_mock.call_args.kwargs == {'credentials': fakecreds1}
        assert ret == fakeservice1
        assert creds_file_mock.call_args.args == (
            '../token.json',
            SCOPES,
        )

        # Test 2: Invalid but refreshable creds
        # check + refresh creds
        os_mock.return_value = True
        os_mock.call_count = 0
        fakecreds2 = MagicMock()
        fakecreds2.valid = False
        fakecreds2.expired = True
        fakecreds2.refresh_token = True
        creds_file_mock.return_value = fakecreds2
        # save refreshed creds
        faketoken2 = MagicMock()
        open_mock.return_value = faketoken2
        # build service
        fakeservice2 = MagicMock()
        build_mock.return_value = fakeservice2

        ret = pc._getservice('1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0')

        assert os_mock.call_count == 1
        assert creds_file_mock.call_count == 2
        assert creds_file_mock.call_args.args == (
            '../token.json',
            SCOPES,
        )
        fakecreds2.refresh.assert_called()  # TODO: check that input is Request() method
        fakecreds2.to_json.assert_called()
        faketoken2.__enter__().write.assert_called_with(fakecreds2.to_json())
        assert build_mock.call_args.args == (
            'docs',
            'v1',
        )
        assert build_mock.call_args.kwargs == {'credentials': fakecreds2}
        assert ret == fakeservice2

        # Test 3: No path to token.json
        # check for path
        os_mock.return_value = False
        os_mock.call_count = 0
        # get flow
        fakeflow3 = MagicMock()
        fakecreds3 = MagicMock()
        fakeflow3.run_local_server.return_value = fakecreds3
        get_secrets_mock.return_value = fakeflow3
        # save refreshed creds
        faketoken3 = MagicMock()
        open_mock.return_value = faketoken3
        # build service
        fakeservice3 = MagicMock()
        build_mock.return_value = fakeservice3

        ret = pc._getservice('1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0', SCOPES)

        assert os_mock.call_count == 2
        assert get_secrets_mock.call_args.args == (
            '../credentials.json',
            SCOPES,
        )
        fakeflow3.run_local_server.assert_called_with(port=0)
        fakecreds3.to_json.assert_called()
        faketoken3.__enter__().write.assert_called_with(fakecreds3.to_json())
        assert build_mock.call_args.args == (
            'docs',
            'v1',
        )
        assert build_mock.call_args.kwargs == {'credentials': fakecreds3}
        assert ret == fakeservice3

        # Test 4: Changing scopes, deleting token.json; HttpError
        # check for path
        os_mock.side_effect = [True, False]
        os_mock.call_count = 0
        os_remove_mock.call_count = 0
        # get flow
        fakeflow4 = MagicMock()
        fakecreds4 = MagicMock()
        fakeflow4.run_local_server.return_value = fakecreds4
        get_secrets_mock.return_value = fakeflow4
        # save refreshed creds
        faketoken4 = MagicMock()
        open_mock.return_value = faketoken4
        # raise error when building service
        build_mock.side_effect = HttpError(resp=MagicMock(), content=b'test')

        ret = pc._getservice('1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0', SCOPES)

        assert os_remove_mock.call_count == 1
        assert os_mock.call_count == 2
        assert get_secrets_mock.call_args.args == (
            '../credentials.json',
            SCOPES,
        )
        fakeflow4.run_local_server.assert_called_with(port=0)
        fakecreds4.to_json.assert_called()
        faketoken4.__enter__().write.assert_called_with(fakecreds4.to_json())
        assert build_mock.call_args.args == (
            'docs',
            'v1',
        )
        assert build_mock.call_args.kwargs == {'credentials': fakecreds4}
        print_mock.assert_called()


def test_smartcopy():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock, patch(
        "prettycopy.prettycopy.trimspacing"
    ) as trim_mock, patch("nltk.tokenize.sent_tokenize") as tokenize_mock, patch(
        "prettycopy.prettycopy._cleanlines"
    ) as cleanlines_mock:
        # Bad type
        paste_mock.return_value = 77
        with pytest.raises(ValueError):
            pc.smartcopy()

        # no newlines in the text
        paste_mock.return_value = "lorem ipsum"
        trim_mock.return_value = "Sentence one. Sentence two."
        tokenize_mock.return_value = ["Sentence one.", "Sentence two."]
        cleanlines_mock.side_effect = ["Sentence one.", "Sentence two."]
        ret = pc.smartcopy()
        assert ret == "Sentence one. Sentence two."
        assert copy_mock.call_args.args == (ret,)

        # newlines
        paste_mock.return_value = "lorem ipsum"
        trim_mock.return_value = "Sentence one.\n Sentence two."
        tokenize_mock.return_value = ["Sentence one.", "Sentence two."]
        cleanlines_mock.side_effect = ["Sentence one.", "Sentence two."]
        ret = pc.smartcopy()
        assert ret == "Sentence one.\nSentence two."
        assert copy_mock.call_args.args == (ret,)

        # text from argument
        trim_mock.return_value = "Sentence one.\n Sentence two."
        tokenize_mock.return_value = ["Sentence one.", "Sentence two."]
        cleanlines_mock.side_effect = ["Sentence one.", "Sentence two."]
        ret = pc.smartcopy("Sentence one.\n Sentence two.")
        assert ret == "Sentence one.\nSentence two."
        assert copy_mock.call_args.args == (ret,)

        assert True


def test_cleanlines():
    with patch("textblob.TextBlob") as textblob_mock, patch("nltk.corpus.words") as words_mock:
        # no space needed
        b1 = MagicMock()
        b1.correct = MagicMock()
        b2 = MagicMock()
        b2.correct = MagicMock()
        textblob_mock.side_effect = [b1, b2]
        b1.correct.side_effect = ["sent", "go"]
        b2.correct.side_effect = ["nice", "is"]
        words_mock.return_value = False
        line = "Sente\nnce 1 goe\ns here."
        ret = pc._cleanlines(line)
        assert ret == "Sentence 1 goes here."

        # space needed
        b1 = MagicMock()
        b1.correct = MagicMock()
        b2 = MagicMock()
        b2.correct = MagicMock()
        textblob_mock.side_effect = [b1, b2]
        b1.correct.side_effect = ["goes"]
        b2.correct.side_effect = ["here"]
        words_mock.return_value = False
        line = "Sentence 2 goes\nhere."
        ret = pc._cleanlines(line)
        assert ret == "Sentence 2 goes here."

        # space needed 2
        b1 = MagicMock()
        b1.correct = MagicMock()
        b2 = MagicMock()
        b2.correct = MagicMock()
        textblob_mock.side_effect = [b1, b2]
        b1.correct.side_effect = ["so"]
        b2.correct.side_effect = ["tense"]
        words_mock.return_value = False
        line = "Se-\r\nntence 3 goes here."
        ret = pc._cleanlines(line)
        assert ret == "Sentence 3 goes here."

        # space not needed 2
        b1 = MagicMock()
        b1.correct = MagicMock()
        b2 = MagicMock()
        b2.correct = MagicMock()
        textblob_mock.side_effect = [b1, b2]
        b1.correct.side_effect = ["Example"]
        b2.correct.side_effect = ["sentence"]
        words_mock.return_value = False
        line = "Example-\r\nsentence 4 goes here."
        ret = pc._cleanlines(line)
        assert ret == "Example-sentence 4 goes here."

        # newline not within a word
        line = "Sentence 5 goes \nhere."
        ret = pc._cleanlines(line)
        assert ret == "Sentence 5 goes here."

        assert True


def test_remove():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        # Bad type
        paste_mock.return_value = 77
        with pytest.raises(ValueError):
            ret = pc.remove('x')

        # Remove from clipboard
        paste_mock.return_value = "Example text here."
        ret = pc.remove('x')
        assert ret == "Eample tet here."
        assert copy_mock.call_args.args == (ret,)

        # Remove from argument
        paste_mock.return_value = None
        ret = pc.remove('e', text="Example text here.")
        assert ret == "Exampl txt hr."
        assert copy_mock.call_args.args == (ret,)

        # Replace
        paste_mock.return_value = "Example text here."
        ret = pc.remove('x', replacement='s')
        assert ret == "Esample test here."
        assert copy_mock.call_args.args == (ret,)


# TODO: test for prettycopy.betterbullets


# CLI testing
def test_app():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        # COPY
        # no gaps
        # clipboard input
        paste_mock.return_value = "Sent\n\n\nence\r\n\r\n one."
        result = runner.invoke(app, ["copy", "--no-gaps"])
        assert result.exit_code == 0
        assert result.stdout == "Sent\nence\n one." + '\n'
        assert copy_mock.call_args.args == ("Sent\nence\n one.",)
        # CLI input
        paste_mock.return_value = None
        result = runner.invoke(app, ["copy", "--no-gaps", "--text", "Testing\n\nsentence\r\n\r\n two here."])
        assert result.exit_code == 0
        assert result.stdout == "Testing\nsentence\n two here." + '\n'
        assert copy_mock.call_args.args == ("Testing\nsentence\n two here.",)

        # removing line breaks (w/o no-bullets)
        paste_mock.return_value = "Testing\nsentence \none."
        result = runner.invoke(app, ["copy", "--no-linebreaks"])
        assert result.exit_code == 0
        assert result.stdout == "Testing sentence one." + "\n"
        assert copy_mock.call_args.args == ("Testing sentence one.",)
        # removing line breaks (w/ no-bullets)
        paste_mock.return_value = "Testing\n•sentence\n• two •here."
        result = runner.invoke(app, ["copy", "--no-linebreaks", "--no-bullets"])
        assert result.exit_code == 0
        assert result.stdout == "Testing sentence two here." + '\n'
        assert copy_mock.call_args.args == ("Testing sentence two here.",)
        # removing bullets (but not line breaks)
        paste_mock.return_value = "•   Te•st• sentence three."
        result = runner.invoke(app, ["copy", "--no-bullets"])
        assert result.exit_code == 0
        assert result.stdout == "Te\nst\nsentence three." + '\n'
        assert copy_mock.call_args.args == ("Te\nst\nsentence three.",)

        # end punct - no quotes
        paste_mock.return_value = "Sentence one"
        result = runner.invoke(app, ["copy", "--end-punct", "!"])
        assert result.exit_code == 0
        assert result.stdout == "Sentence one!" + '\n'
        assert copy_mock.call_args.args == ("Sentence one!",)
        # end punct - quotes
        paste_mock.return_value = "\"Sentence two\""
        result = runner.invoke(app, ["copy", "--end-punct", "!"])
        assert result.exit_code == 0
        assert result.stdout == "\"Sentence two!\"" + '\n'
        assert copy_mock.call_args.args == ("\"Sentence two!\"",)
        # line punct
        paste_mock.return_value = "apples\noranges \n pears"
        result = runner.invoke(app, ["copy", "--line-punct", ";"])
        assert result.exit_code == 0
        assert result.stdout == "apples; oranges; pears" + '\n'
        assert copy_mock.call_args.args == ("apples; oranges; pears",)
        # bullet punct
        paste_mock.return_value = "\n•apples\n    •    oranges\n • pears"
        result = runner.invoke(app, ["copy", "--bullet-punct", ";"])
        assert result.exit_code == 0
        assert result.stdout == "apples; oranges; pears" + '\n'
        assert copy_mock.call_args.args == ("apples; oranges; pears",)
        # quote
        paste_mock.return_value = "Sentence three"
        result = runner.invoke(app, ["copy", "--quote"])
        assert result.exit_code == 0
        assert result.stdout == "\"Sentence three\"" + '\n'
        assert copy_mock.call_args.args == ("\"Sentence three\"",)
        # quote + end punct
        paste_mock.return_value = "Sentence four"
        result = runner.invoke(app, ["copy", "--quote", "--end-punct", ","])
        assert result.exit_code == 0
        assert result.stdout == "\"Sentence four,\"" + '\n'
        assert copy_mock.call_args.args == ("\"Sentence four,\"",)

        # replace
        paste_mock.return_value = "Sentence one."
        result = runner.invoke(app, ["copy", "--replace", "e", "x"])
        assert result.exit_code == 0
        assert result.stdout == "Sxntxncx onx." + '\n'
        assert copy_mock.call_args.args == ("Sxntxncx onx.",)
        # remove
        paste_mock.return_value = "Sentence two."
        result = runner.invoke(app, ["copy", "--remove", "e"])
        assert result.exit_code == 0
        assert result.stdout == "Sntnc two." + '\n'
        assert copy_mock.call_args.args == ("Sntnc two.",)
        # case: lower
        paste_mock.return_value = "SenTEnCe thREE."
        result = runner.invoke(app, ["copy", "--case", "lower"])
        assert result.exit_code == 0
        assert result.stdout == "sentence three." + '\n'
        assert copy_mock.call_args.args == ("sentence three.",)
        # case: upper
        paste_mock.return_value = "SenTEnCe fOUr."
        result = runner.invoke(app, ["copy", "--case", "upper"])
        assert result.exit_code == 0
        assert result.stdout == "SENTENCE FOUR." + '\n'
        assert copy_mock.call_args.args == ("SENTENCE FOUR.",)
        # case: title
        paste_mock.return_value = "SenTEnCe fIvE."
        result = runner.invoke(app, ["copy", "--case", "title"])
        assert result.exit_code == 0
        assert result.stdout == "Sentence Five." + '\n'
        assert copy_mock.call_args.args == ("Sentence Five.",)
        # case: capital
        paste_mock.return_value = "SenTEnCe sIx. hErE it iS."
        result = runner.invoke(app, ["copy", "--case", "capital"])
        assert result.exit_code == 0
        assert result.stdout == "Sentence six. Here it is." + '\n'
        assert copy_mock.call_args.args == ("Sentence six. Here it is.",)

        # no output
        paste_mock.return_value = "Sentence one."
        result = runner.invoke(app, ["copy", "--no-output"])
        assert result.exit_code == 0
        assert result.stdout == ''
        assert copy_mock.call_args.args == ("Sentence one.",)

        # no new lines
        # clipboard input
        paste_mock.return_value = "Testing\nsentence one \nhere."
        result = runner.invoke(app, ["nonewlines"])
        assert result.exit_code == 0
        assert result.stdout == "Testing sentence one here." + '\n'
        assert copy_mock.call_args.args == ("Testing sentence one here.",)
        # text input
        paste_mock.return_value = None
        result = runner.invoke(app, ["nonewlines", "--text", "Testing\nsentence two \nhere."])
        assert result.exit_code == 0
        assert result.stdout == "Testing sentence two here." + '\n'
        assert copy_mock.call_args.args == ("Testing sentence two here.",)
        # error
        paste_mock.return_value = 42
        result = runner.invoke(app, ["nonewlines"])
        assert result.exit_code == 0
        assert result.stdout == typer.style("Input should have been a string!", fg="white", bg="red") + '\n'
        # no-output
        paste_mock.return_value = "Testing\nsentence three \nhere."
        result = runner.invoke(app, ["nonewlines", "--no-output"])
        assert result.exit_code == 0
        assert result.stdout == ''
        assert copy_mock.call_args.args == ("Testing sentence three here.",)

        # no bullets
        # clipboard input
        paste_mock.return_value = "•   Te•st• Test"
        result = runner.invoke(app, ["bullettolist"])
        assert result.exit_code == 0
        assert result.stdout == "Te\nst\nTest" + '\n'
        assert copy_mock.call_args.args == ("Te\nst\nTest",)
        # text input
        paste_mock.return_value = None
        result = runner.invoke(app, ["bullettolist", "--text", "•test"])
        assert result.exit_code == 0
        assert result.stdout == "test" + '\n'
        assert copy_mock.call_args.args == ("test",)
        # error
        paste_mock.return_value = 42
        result = runner.invoke(app, ["bullettolist"])
        assert result.exit_code == 0
        assert result.stdout == typer.style("Input should have been a string!", fg="white", bg="red") + '\n'
        # no-output
        paste_mock.return_value = "•   Te•st• Test"
        result = runner.invoke(app, ["bullettolist", "--no-output"])
        assert result.exit_code == 0
        assert result.stdout == ''
        assert copy_mock.call_args.args == ("Te\nst\nTest",)

        # bullet to par
        # clipboard input
        paste_mock.return_value = "Testing\n•sentence\n• one •here."
        result = runner.invoke(app, ["bullettopar"])
        assert result.exit_code == 0
        assert result.stdout == "Testing sentence one here." + '\n'
        assert copy_mock.call_args.args == ("Testing sentence one here.",)
        # text input
        paste_mock.return_value = None
        result = runner.invoke(app, ["bullettopar", "--text", "Testing\n•sentence\n• two •here."])
        assert result.exit_code == 0
        assert result.stdout == "Testing sentence two here." + '\n'
        assert copy_mock.call_args.args == ("Testing sentence two here.",)
        # error
        paste_mock.return_value = 42
        result = runner.invoke(app, ["bullettopar"])
        assert result.exit_code == 0
        assert result.stdout == typer.style("Input should have been a string!", fg="white", bg="red") + '\n'
        # no-output
        paste_mock.return_value = "Testing\n•sentence\n• three •here."
        result = runner.invoke(app, ["bullettopar", "--no-output"])
        assert result.exit_code == 0
        assert result.stdout == ''
        assert copy_mock.call_args.args == ("Testing sentence three here.",)

        # simple quote
        # clipboard input
        paste_mock.return_value = 'Testing sentence one here.'
        result = runner.invoke(app, ["simplequote"])
        assert result.exit_code == 0
        assert result.stdout == '"Testing sentence one here."' + '\n'
        assert copy_mock.call_args.args == ('"Testing sentence one here."',)
        # text input
        paste_mock.return_value = None
        result = runner.invoke(app, ["simplequote", "--text", 'Testing sentence two here.'])
        assert result.exit_code == 0
        assert result.stdout == '"Testing sentence two here."' + '\n'
        assert copy_mock.call_args.args == ('"Testing sentence two here."',)
        # error
        paste_mock.return_value = 42
        result = runner.invoke(app, ["simplequote"])
        assert result.exit_code == 0
        assert result.stdout == typer.style("Input should have been a string!", fg="white", bg="red") + '\n'
        # no-output
        paste_mock.return_value = 'Testing sentence three here.'
        result = runner.invoke(app, ["simplequote", "--no-output"])
        assert result.exit_code == 0
        assert result.stdout == ''
        assert copy_mock.call_args.args == ('"Testing sentence three here."',)

        # quote
        # clipboard only
        paste_mock.return_value = 'Testing sentence one here'
        result = runner.invoke(app, ["quote"])
        assert result.exit_code == 0
        assert result.stdout == '"Testing sentence one here"' + '\n'
        assert copy_mock.call_args.args == ('"Testing sentence one here"',)
        # text only
        paste_mock.return_value = None
        result = runner.invoke(app, ["quote", "--text", 'Testing sentence two here'])
        assert result.exit_code == 0
        assert result.stdout == '"Testing sentence two here"' + '\n'
        assert copy_mock.call_args.args == ('"Testing sentence two here"',)
        # clipboard + punc only
        paste_mock.return_value = 'Testing sentence three here'
        result = runner.invoke(app, ["quote", "!"])
        assert result.exit_code == 0
        assert result.stdout == '"Testing sentence three here!"' + '\n'
        assert copy_mock.call_args.args == ('"Testing sentence three here!"',)
        # text + punc
        paste_mock.return_value = None
        result = runner.invoke(app, ["quote", "?", "--text", 'Testing sentence four here'])
        assert result.exit_code == 0
        assert result.stdout == '"Testing sentence four here?"' + '\n'
        assert copy_mock.call_args.args == ('"Testing sentence four here?"',)
        # no-output
        paste_mock.return_value = 'Testing sentence five here'
        result = runner.invoke(app, ["quote", "--no-output"])
        assert result.exit_code == 0
        assert result.stdout == ''
        assert copy_mock.call_args.args == ('"Testing sentence five here"',)

        # trim spacing
        # clipboard input
        paste_mock.return_value = "Testing\n\nsentence\r\n\r\n one here."
        result = runner.invoke(app, ["trimspacing"])
        assert result.exit_code == 0
        assert result.stdout == "Testing\nsentence\n one here." + '\n'
        assert copy_mock.call_args.args == ("Testing\nsentence\n one here.",)
        # text input
        paste_mock.return_value = None
        result = runner.invoke(app, ["trimspacing", "--text", "Testing\n\nsentence\r\n\r\n two here."])
        assert result.exit_code == 0
        assert result.stdout == "Testing\nsentence\n two here." + '\n'
        assert copy_mock.call_args.args == ("Testing\nsentence\n two here.",)
        # error
        paste_mock.return_value = 42
        result = runner.invoke(app, ["trimspacing"])
        assert result.exit_code == 0
        assert result.stdout == typer.style("Input should have been a string!", fg="white", bg="red") + '\n'
        # no-output
        paste_mock.return_value = "Testing\n\nsentence\r\n\r\n three here."
        result = runner.invoke(app, ["trimspacing", "--no-output"])
        assert result.exit_code == 0
        assert result.stdout == ''
        assert copy_mock.call_args.args == ("Testing\nsentence\n three here.",)

        # smart copy
        # clipboard input
        paste_mock.return_value = "Testing se\nntence one\nhere."
        result = runner.invoke(app, ["smartcopy"])
        assert result.exit_code == 0
        assert result.stdout == "Testing sentence one here." + '\n'
        assert copy_mock.call_args.args == ("Testing sentence one here.",)
        # text input
        paste_mock.return_value = None
        result = runner.invoke(app, ["smartcopy", "--text", "Testing se\nntence two\nhere."])
        assert result.exit_code == 0
        assert result.stdout == "Testing sentence two here." + '\n'
        assert copy_mock.call_args.args == ("Testing sentence two here.",)
        # error
        paste_mock.return_value = 42
        result = runner.invoke(app, ["smartcopy"])
        assert result.exit_code == 0
        assert result.stdout == typer.style("Input should have been a string!", fg="white", bg="red") + '\n'
        # no-output
        paste_mock.return_value = "Testing se\nntence three\nhere."
        result = runner.invoke(app, ["smartcopy", "--no-output"])
        assert result.exit_code == 0
        assert result.stdout == ''
        assert copy_mock.call_args.args == ("Testing sentence three here.",)

        # remove
        # clipboard input - remove
        paste_mock.return_value = "Testing sentence one here."
        result = runner.invoke(app, ["remove", "one"])
        assert result.exit_code == 0
        assert result.stdout == "Testing sentence  here." + '\n'
        assert copy_mock.call_args.args == ("Testing sentence  here.",)
        # text input - remove
        paste_mock.return_value = None
        result = runner.invoke(app, ["remove", "sen", "--text", "Testing sentence two here."])
        assert result.exit_code == 0
        assert result.stdout == "Testing tence two here." + '\n'
        assert copy_mock.call_args.args == ("Testing tence two here.",)
        # clipboard input - replace
        paste_mock.return_value = "Testing sentence three here."
        result = runner.invoke(app, ["remove", "en", "--replacement", "EN"])
        assert result.exit_code == 0
        assert result.stdout == "Testing sENtENce three here." + '\n'
        assert copy_mock.call_args.args == ("Testing sENtENce three here.",)
        # text input - replace
        paste_mock.return_value = None
        result = runner.invoke(
            app, ["remove", "four", "--replacement", "twenty", "--text", "Testing sentence four here."]
        )
        assert result.exit_code == 0
        assert result.stdout == "Testing sentence twenty here." + '\n'
        assert copy_mock.call_args.args == ("Testing sentence twenty here.",)
        # error
        paste_mock.return_value = 42
        result = runner.invoke(app, ["remove", "x"])
        assert result.exit_code == 0
        assert result.stdout == typer.style("Input should have been a string!", fg="white", bg="red") + '\n'
        # no-output
        paste_mock.return_value = "Testing sentence five here."
        result = runner.invoke(app, ["remove", "here", "--no-output"])
        assert result.exit_code == 0
        assert result.stdout == ''
        assert copy_mock.call_args.args == ("Testing sentence five .",)
