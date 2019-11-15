from helpers import get_color, message_formatter, post_on_slack


def test_get_color_zero_fails():
    color = get_color(0)
    assert color == '#36a64f'


def test_get_color_one_fail():
    color = get_color(1)
    assert color == '#FC736A'


def test_message_formatter_success():
    message = message_formatter(10, 0, 0, 'chrome')
    assert message == 'chrome: 10 tests passed'


def test_message_formatter_one_primary_fail():
    message = message_formatter(10, 1, 1, 'chrome')
    assert message == 'chrome: 1 test failed (1 primary)'


def test_message_formatter_one_secondary_fail():
    message = message_formatter(10, 1, 0, 'chrome')
    assert message == 'chrome: 1 test failed (0 primaries)'


def test_message_formatter_two_fails():
    message = message_formatter(10, 2, 1, 'chrome')
    assert message == 'chrome: 2 tests failed (1 primary)'


def test_message_formatter_three_fails():
    message = message_formatter(10, 3, 2, 'chrome')
    assert message == 'chrome: 3 tests failed (2 primaries)'
