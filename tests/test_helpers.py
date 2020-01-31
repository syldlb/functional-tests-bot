import requests
from unittest.mock import patch
from bot.helpers import get_color, message_formatter, validate_args, auth_get


def test_check_args_valid():
    args = ["", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    assert validate_args(args)


def test_check_args_invalid():
    args = ["", "1", "2", "3", "4", "5", "6", "7", "8"]
    assert not validate_args(args)


def test_get_color_zero_fails():
    color = get_color(0, 0, "true")
    assert color == "#36a64f"


def test_get_color_one_secondary_fail():
    color = get_color(1, 0, "true")
    assert color == "#FFBF00"


def test_get_color_one_secondary_fail_no_primaries():
    color = get_color(1, 0, "false")
    assert color == "#FC736A"


def test_get_color_one_primary_fail():
    color = get_color(1, 1, "true")
    assert color == "#FC736A"


def test_get_color_two_fails():
    color = get_color(2, 1, "true")
    assert color == "#FC736A"


def test_message_formatter_success():
    message = message_formatter(10, 0, 0, "chrome", "true")
    assert message == "chrome: 10 tests passed"


def test_message_formatter_one_primary_fail():
    message = message_formatter(10, 1, 1, "chrome", "true")
    assert message == "chrome: 1 test failed (1 primary)"


def test_message_formatter_one_secondary_fail():
    message = message_formatter(10, 1, 0, "chrome", "true")
    assert message == "chrome: 1 test failed (0 primaries)"


def test_message_formatter_two_fails():
    message = message_formatter(10, 2, 1, "chrome", "true")
    assert message == "chrome: 2 tests failed (1 primary)"


def test_message_formatter_three_fails():
    message = message_formatter(10, 3, 2, "chrome", "true")
    assert message == "chrome: 3 tests failed (2 primaries)"


def test_message_formatter_three_fails_no_primaries():
    message = message_formatter(10, 3, 2, "chrome", "false")
    assert message == "chrome: 3 tests failed"


def test_auth_get():
    with patch("bot.helpers.requests.get") as mock_get:
        auth_get("http://fake_url", "usrnm", "pwd")
        auth_b64 = requests.auth.HTTPBasicAuth("usrnm", "pwd")
        mock_get.assert_called_once_with("http://fake_url", auth=auth_b64)
