import requests
import sys

from bot.helpers import (
    message_formatter,
    get_color,
    validate_args,
)
from bot.jenkins import get_tests_list, get_run_detail_response
from bot.giphy import get_random_gif_url
from bot.slack import post_on_slack


def run(args):

    if not validate_args(args):
        sys.exit(1)

    user = args[1]
    password = args[2]
    giphy_key = args[3]
    jenkins_url = args[4]
    job_name = args[5]
    hook_url = args[6]
    browser = args[7]
    use_primaries = args[8]
    gif_category = args[9]

    try:
        project_response = get_tests_list(jenkins_url, job_name, user, password)

        # get each test status
        fails_number = 0
        primary_fails_number = 0
        tests_number = 0
        for run_detail in project_response.json()["runs"]:
            if browser in run_detail["url"]:
                tests_number = tests_number + 1
                run_detail_response = get_run_detail_response(
                    run_detail["url"], user, password
                )
                if run_detail_response.json()["result"] == "FAILURE":
                    fails_number = fails_number + 1
                    if "primary" in run_detail["url"]:
                        primary_fails_number = primary_fails_number + 1
        print("fails number: %s" % fails_number)
        print("number total of tests: %s" % tests_number)
        print("primary_fails_number: %s" % primary_fails_number)

        # send summary on slack
        if fails_number == 0 and gif_category != "no_gif":
            gif_url = get_random_gif_url(gif_category, giphy_key)
        else:
            gif_url = None
        message = message_formatter(
            tests_number, fails_number, primary_fails_number, browser, use_primaries
        )
        color = get_color(fails_number, primary_fails_number, use_primaries)
        post_on_slack(jenkins_url, hook_url, job_name, message, color, gif_url)
        sys.exit(0)

    except requests.exceptions.HTTPError as http_err:
        print("HTTP error occurred: %s" % http_err)
    except Exception as err:
        print("Unexpected error occurred: %s" % err)
