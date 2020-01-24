import requests
import json
import random


def get_random_gif_url(category, giphy_key):
    random_index = random.randint(0, 24)
    params = {"api_key": giphy_key, "q": category}
    url = "https://api.giphy.com/v1/gifs/search"
    r = requests.get(url, params)
    gifs_json = r.json()
    gif_url = gifs_json["data"][random_index]["images"]["downsized"]["url"]
    return gif_url


def message_formatter(
    tests_number, fails_number, primary_fails_number, browser, use_primaries
):
    message = browser + ": "
    if fails_number == 0:
        message = message + "%s tests passed" % (tests_number)
        return message

    tests_string = "test" if fails_number == 1 else "tests"
    message = message + "%s %s failed" % (fails_number, tests_string)
    if use_primaries == "true":
        primary_str = "primary" if primary_fails_number == 1 else "primaries"
        message = message + " (%s %s)" % (primary_fails_number, primary_str)
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


def post_on_slack(jenkins_url, hook_url, job_name, message, color, gif_url):
    tests_url = jenkins_url + "job/" + job_name
    data = dict()
    data["attachments"] = [
        {
            "fallback": message,
            "color": color,
            "title": job_name,
            "title_link": tests_url,
            "text": message,
        }
    ]
    if gif_url:
        data["attachments"][0]["image_url"] = gif_url
    data_string = json.dumps(data)
    print(data_string)
    requests.post(hook_url, data=data_string)
