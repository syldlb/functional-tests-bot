#!/usr/bin/python

import requests
import sys

from helpers import auth_get, message_formatter, get_color, post_on_slack

if len(sys.argv) != 7:
    print('Incorrect number of argument.\n'
          'Usage python3.5 script.py [username] [password] [jenkins_url] '
          '[job_name] [hook_utl] [browser]')
    sys.exit(1)

user = sys.argv[1]
password = sys.argv[2]
jenkins_url = sys.argv[3]
job_name = sys.argv[4]
hook_url = sys.argv[5]
browser = sys.argv[6]


try:
    # get the list of tests
    project_url = jenkins_url + 'job/' + job_name + '/lastBuild/api/json'
    project_response = auth_get(project_url, user, password)
    print('response code: %s' % project_response.status_code)

    # get each test status
    fails_number = 0
    primary_fails_number = 0
    tests_number = 0
    for run_detail in project_response.json()['runs']:
        if browser in run_detail['url']:
            tests_number = tests_number + 1
            run_detail_url = run_detail['url'] + 'api/json'
            run_detail_response = auth_get(run_detail_url, user, password)
            if run_detail_response.json()['result'] == 'FAILURE':
                fails_number = fails_number + 1
                if 'primary' in run_detail['url']:
                    primary_fails_number = primary_fails_number + 1
    print('fails number: %s' % fails_number)
    print('number total of tests: %s' % tests_number)
    print('primary_fails_number: %s' % primary_fails_number)

    # send summary on slack
    message = message_formatter(
        tests_number, fails_number, primary_fails_number, browser)
    color = get_color(fails_number)
    post_on_slack(jenkins_url, hook_url, job_name, message, color)
    sys.exit(0)

except requests.exceptions.HTTPError as http_err:
    print('HTTP error occurred: %s' % http_err)
except Exception as err:
    print('Unexpected error occurred: %s' % err)
