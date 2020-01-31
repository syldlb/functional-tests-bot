import requests


def validate_args(args):
    if len(args) != 10:
        print(
            "Incorrect number of argument.\n"
            "Usage python3.6 main.py [username] [password] [giphy_key] "
            "[jenkins_url] [job_name] [hook_url] [browser] [use_primaries] "
            "[gif_category]"
        )
        return False
    return True


def message_formatter(
    tests_number, fails_number, primary_fails_number, browser, use_primaries
):
    message = browser + ": "
    if fails_number == 0:
        message = f"{message}{tests_number} tests passed"
        return message

    tests_string = "test" if fails_number == 1 else "tests"
    message = f"{message}{fails_number} {tests_string} failed"
    if use_primaries == "true":
        primary_str = "primary" if primary_fails_number == 1 else "primaries"
        message = f"{message} ({primary_fails_number} {primary_str})"
    return message


def get_color(fails_number, primary_fails_number, use_primaries):
    if fails_number == 0:
        return "#36a64f"
    elif use_primaries == "true" and primary_fails_number == 0:
        return "#FFBF00"
    else:
        return "#FC736A"


def auth_get(url, user, password):
    r = requests.get(url, auth=requests.auth.HTTPBasicAuth(user, password))
    return r
