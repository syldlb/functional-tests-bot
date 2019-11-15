#!/usr/bin/python

import requests
import sys
import json

if len(sys.argv) != 6:
    print('''Incorrect number of argument.
             Usage python script.py [username] [password] [jenkins_url] [job_name] [hook_utl]''')
    sys.exit(1)

user = sys.argv[1]
password = sys.argv[2]
jenkins_url = sys.argv[3]
job_name = sys.argv[4]
hook_url = sys.argv[5]


def auth_get(url):
    r = requests.get(url, auth=requests.auth.HTTPBasicAuth(user, password))
    return r


def post_on_slack(message, color):
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
    r = requests.post(hook_url, data=data_string)
    return r


def message_formatter(tests_number, fails_number, primary_fails_number):
    message = ''
    if fails_number == 0:
        message = message + '%s tests passed' % (tests_number)
    else:
        tests_string = "test" if fails_number == 1 else "tests"
        primaries_string = "primary" if primary_fails_number == 1 else "primaries"
        message = message + '%s %s failed (%s %s)' % (fails_number, tests_string, primary_fails_number, primaries_string)
    return message


def get_color(fails_number):
    if fails_number == 0:
        return '#36a64f'
    else:
        return '#FC736A'


try:
    # get the list of tests
    project_url = jenkins_url + 'job/' + job_name + '/lastBuild/api/json'
    project_response = auth_get(project_url)
    print('response code: %s' % project_response.status_code)

    # get each test status
    fails_number = 0
    primary_fails_number = 0
    tests_number = 0
    for run_detail in project_response.json()['runs']:
        if 'chrome' in run_detail['url']:
            tests_number = tests_number + 1
            run_detail_url = run_detail['url'] + 'api/json'
            run_detail_response = auth_get(run_detail_url)
            if run_detail_response.json()['result'] == 'FAILURE':
                fails_number = fails_number + 1
                if 'primary' in run_detail['url']:
                    primary_fails_number = primary_fails_number + 1
    print('fails number: %s' % fails_number)
    print('number total of tests: %s' % tests_number)
    print('primary_fails_number: %s' % primary_fails_number)

    # send summary on slack
    message = message_formatter(
        tests_number, fails_number, primary_fails_number)
    color = get_color(fails_number)
    post_on_slack(message, color)
    sys.exit(0)

except requests.exceptions.HTTPError as http_err:
    print('HTTP error occurred: %s' % http_err)
except Exception as err:
    print('Unexpected error occurred: %s' % err)
