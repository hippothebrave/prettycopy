# import prettycopy as pc
import prettycopy.prettycopy as pc
from prettycopy.gdocs import getservice

# from prettycopy import nonewlines, nobullets, bullettopar, quote, simplequote
from unittest.mock import patch, MagicMock
from googleapiclient.errors import HttpError


def test_nonewlines():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        # Text from clipboard
        paste_mock.return_value = "Testing\n line \nof text\n here."
        ret = pc.nonewlines()
        assert ret == "Testing line of text here."
        assert copy_mock.call_args.args == (ret,)

        # Text from argument
        ret = pc.nonewlines("Another\n line \nof text\n here.")
        assert ret == "Another line of text here."
        assert copy_mock.call_args.args == (ret,)


def test_nobullets():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock, patch(
        "prettycopy.prettycopy.nonewlines"
    ) as newline_mock:
        # No spaces
        paste_mock.return_value = "•Test\n•Test"
        newline_mock.return_value = "•Test•Test"
        ret = pc.nobullets()
        newline_mock.assert_called_once()
        assert newline_mock.call_args.args == ()
        assert ret == "Test\nTest"
        assert copy_mock.call_args.args == (ret,)

        # Spaces between bullet and text
        paste_mock.return_value = "• Test\n• Test"
        newline_mock.return_value = "• Test• Test"
        ret = pc.nobullets()
        assert newline_mock.call_args.args == ()
        assert ret == "Test\nTest"
        assert copy_mock.call_args.args == (ret,)

        # Bullets within words
        paste_mock.return_value = "•   Te•st• Test"
        newline_mock.return_value = "•   Te•st• Test"
        ret = pc.nobullets()
        assert newline_mock.call_args.args == ()
        assert ret == "Te\nst\nTest"
        assert copy_mock.call_args.args == (ret,)

        # Text from argument
        newline_mock.return_value = "•Another•Test"
        ret = pc.nobullets("•Another\n•Test")
        assert newline_mock.call_args.args == ()
        assert ret == "Another\nTest"
        assert copy_mock.call_args.args == (ret,)


def test_bullettopar():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        # No spaces
        paste_mock.return_value = "•Test\n•Test"
        ret = pc.bullettopar()
        assert ret == "Test Test"
        assert copy_mock.call_args.args == (ret,)

        # Spaces after bullets
        paste_mock.return_value = "• Test\n• Test"
        ret = pc.bullettopar()
        assert ret == "Test Test"
        assert copy_mock.call_args.args == (ret,)

        # Bullets within words
        paste_mock.return_value = "•   Te•st• Test"
        ret = pc.bullettopar()
        assert ret == "Te st Test"
        assert copy_mock.call_args.args == (ret,)

        # Text from argument
        ret = pc.bullettopar("•Another\n•Test")
        assert ret == "Another Test"
        assert copy_mock.call_args.args == (ret,)


def test_simplequote():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        # Argument from clipboard
        paste_mock.return_value = 'Test test'
        ret = pc.simplequote()
        assert ret == '"Test test"'
        assert copy_mock.call_args.args == (ret,)

        # Text from argument
        ret = pc.simplequote('Another test')
        assert ret == '"Another test"'
        assert copy_mock.call_args.args == (ret,)


# TODO: check ValueErrors
def test_quote():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        # No arguments
        paste_mock.return_value = 'Test test'
        ret = pc.quote()
        assert ret == '"Test test,"'
        assert copy_mock.call_args.args == (ret,)

        # Punctuation argument
        paste_mock.return_value = 'Test test'
        ret = pc.quote('.')
        assert ret == '"Test test."'
        assert copy_mock.call_args.args == (ret,)

        # Text argument
        ret = pc.quote(text='Another test')
        assert ret == '"Another test,"'
        assert copy_mock.call_args.args == (ret,)

        # Text and punctuation argument
        ret = pc.quote('!', 'Another test')
        assert ret == '"Another test!"'
        assert copy_mock.call_args.args == (ret,)

        # Incorrect punctuation argument
        paste_mock.return_value = 'Test test'
        try:
            ret = pc.quote('test')
            assert True == False  # noqa E712
        except ValueError:
            assert len('test') > 1

        # Incorrect punctuation argument
        paste_mock.return_value = 'Test test'
        try:
            ret = pc.quote(';')
            assert True == False  # noqa E712
        except ValueError:
            assert ';' not in [',', '.', '!', '?']


# TODO: check that HTTPError is printed in Test 4
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
        build_mock.return_value = fakeservice1  # FIXME there was an issue here

        ret = getservice('1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0')

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

        ret = getservice('1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0')

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

        ret = getservice('1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0', SCOPES)

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

        ret = getservice('1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0', SCOPES)

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


# TODO: test for prettycopy.betterbullets
# def test_betterbullets():
#     with patch("prettycopy.nobullets") as nobullets_mock:
#         nobullets_mock.return_value = "Test\ncontent\nhere"
#         service = getservice()

#         # find end of current google doc content
#         document = service.documents().get(documentId="1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0").execute()
#         doclines = document.get('body')['content']
#         content = ""
#         for line in doclines[1:]:
#             content += line['paragraph']['elements'][0]['textRun']['content']
#         originalEnding = len(content)

#         #run function
#         pc.betterbullets("1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0")

#         # find end of current google doc content
#         document = service.documents().get(documentId="1yxH3v4zi82pEMKW41MbZRqKz8JXRbhrb5yJnEdSfJC0").execute()
#         doclines = document.get('body')['content']
#         content2 = ""
#         for line in doclines[1:]:
#             content2 += line['paragraph']['elements'][0]['textRun']['content']
#         newEnding = len(content2)

#         assert originalEnding + len("Test\ncontent\nhere") == newEnding
