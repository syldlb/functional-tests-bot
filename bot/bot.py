import requests
import sys

from bot.helpers import (
    auth_get,
    message_formatter,
    get_color,
    post_on_slack,
    get_random_gif_url,
)


def run(args):

    if len(args) != 10:
        print(
            "Incorrect number of argument.\n"
            "Usage python3.6 main.py [username] [password] [giphy_key] "
            "[jenkins_url] [job_name] [hook_url] [browser] [use_primaries] "
            "[gif_category]"
        )
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
        # get the list of tests
        project_url = f"{jenkins_url}job/{job_name}/lastBuild/api/json"
        project_response = auth_get(project_url, user, password)
        print("response code: %s" % project_response.status_code)

        # get each test status
        fails_number = 0
        primary_fails_number = 0
        tests_number = 0
        for run_detail in project_response.json()["runs"]:
            if browser in run_detail["url"]:
                tests_number = tests_number + 1
                run_detail_url = run_detail["url"] + "api/json"
                run_detail_response = auth_get(run_detail_url, user, password)
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
