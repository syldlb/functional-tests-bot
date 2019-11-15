import requests
import json


def message_formatter(tests_number, fails_number, primary_fails_number):
    message = ''
    if fails_number == 0:
        message = message + '%s tests passed' % (tests_number)
        return message

    tests_string = "test" if fails_number == 1 else "tests"
    primary_string = "primary" if primary_fails_number == 1 else "primaries"
    message = message + '%s %s failed (%s %s)' % (
        fails_number, tests_string, primary_fails_number, primary_string)
    return message


def get_color(fails_number):
    if fails_number == 0:
        return '#36a64f'
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
