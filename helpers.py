import requests
import json


def message_formatter(
        tests_number, fails_number, primary_fails_number, browser,
        use_primaries):
    message = browser + ': '
    if fails_number == 0:
        message = message + '%s tests passed' % (tests_number)
        return message

    tests_string = "test" if fails_number == 1 else "tests"
    message = message + '%s %s failed' % (
        fails_number, tests_string)
    if use_primaries == 'true':
        primary_str = "primary" if primary_fails_number == 1 else "primaries"
        message = message + ' (%s %s)' % (primary_fails_number, primary_str)
    return message


def get_color(fails_number, primary_fails_number, use_primaries):
    if fails_number == 0:
        return '#36a64f'
    elif use_primaries == 'true' and primary_fails_number == 0:
        return '#FFBF00'
    else:
        return '#FC736A'


def auth_get(url, user, password):
    r = requests.get(url, auth=requests.auth.HTTPBasicAuth(user, password))
    return r


def post_on_slack(jenkins_url, hook_url, job_name, message, color):
    tests_url = jenkins_url + 'job/' + job_name
    data = dict()
    data['attachments'] = [{
            "fallback": message,
            "color": color,
            "title": job_name,
            "title_link": tests_url,
            "text": message
        }]
    data_string = json.dumps(data)
    print(data_string)
    requests.post(hook_url, data=data_string)
