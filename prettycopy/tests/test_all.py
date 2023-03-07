from prettycopy.mytest import nonewlines, nobullets, bullettopar, quote
from prettycopy.gdocs import getservice, SCOPES
from unittest.mock import patch, MagicMock


def test_nonewlines():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        paste_mock.return_value = "Testing\n line \nof text\n here."
        ret = nonewlines()
        assert ret == "Testing line of text here."
        assert copy_mock.call_args.args == (ret,)


def test_nobullets():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock, patch(
        "mytest.nonewlines"
    ) as newline_mock:
        paste_mock.return_value = "•Test\n•Test"
        newline_mock.return_value = "•Test•Test"
        ret = nobullets()
        assert newline_mock.call_args == None  # noqa: E711
        assert ret == "Test\nTest"
        assert copy_mock.call_args.args == (ret,)

        paste_mock.return_value = "• Test\n• Test"
        newline_mock.return_value = "• Test• Test"
        ret = nobullets()
        assert newline_mock.call_args == None  # noqa: E711
        assert ret == "Test\nTest"
        assert copy_mock.call_args.args == (ret,)

        paste_mock.return_value = "•   Te•st• Test"
        newline_mock.return_value = "•   Te•st• Test"
        ret = nobullets()
        assert newline_mock.call_args == None  # noqa: E711
        assert ret == "Te\nst\nTest"
        assert copy_mock.call_args.args == (ret,)


def test_bullettopar():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        paste_mock.return_value = "•Test\n•Test"
        ret = bullettopar()
        assert ret == "Test Test"
        assert copy_mock.call_args.args == (ret,)

        paste_mock.return_value = "• Test\n• Test"
        ret = bullettopar()
        assert ret == "Test Test"
        assert copy_mock.call_args.args == (ret,)

        paste_mock.return_value = "•   Te•st• Test"
        ret = bullettopar()
        assert ret == "Te st Test"
        assert copy_mock.call_args.args == (ret,)


def test_quote():
    with patch("pyperclip.copy") as copy_mock, patch("pyperclip.paste") as paste_mock:
        paste_mock.return_value = 'Test test'
        ret = quote()
        assert ret == '"Test test"'
        assert copy_mock.call_args.args == (ret,)

        paste_mock.return_value = 'Test test'
        ret = quote(True)
        assert ret == '"Test test,"'
        assert copy_mock.call_args.args == (ret,)


def test_getservice():
    # also need to mock creds, "flow" result of InstalledAppFlow, token file with write() method
    with patch("os.path.exists") as os_mock, patch(
        "google.oauth2.credentials.Credentials.from_authorized_user_file"
    ) as creds_file_mock, patch(
        "google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file"
    ) as get_secrets_mock, patch(
        "builtins.open"
    ) as open_mock, patch(
        "googleapiclient.discovery.build"
    ) as build_mock:  # patch("gdocs.build") as build2_mock:
        # Test 1: credentials do exist
        # check + get creds
        os_mock.return_value = True
        fakecreds1 = MagicMock()
        fakecreds1.valid = True
        creds_file_mock.return_value = fakecreds1
        # build service
        fakeservice1 = MagicMock()
        build_mock.return_value = fakeservice1  # FIXME there was an issue here

        ret = getservice()

        assert os_mock.call_count == 1
        assert creds_file_mock.call_count == 1
        assert build_mock.call_args.args == (
            'docs',
            'v1',
        )
        assert build_mock.call_args.kwargs == {'credentials': fakecreds1}
        assert ret == fakeservice1

        # Test 2: Invalid but refreshable creds
        # check + refresh creds
        os_mock.return_value = True
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

        ret = getservice()

        assert os_mock.call_count == 2
        assert creds_file_mock.call_count == 2
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

        ret = getservice()

        assert os_mock.call_count == 3
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


# TODO: test for mytest.betterbullets
