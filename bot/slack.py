import requests
import json


def post_on_slack(jenkins_url, hook_url, job_name, message, color, gif_url):
    tests_url = f"{jenkins_url}job/{job_name}"
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
    return requests.post(hook_url, data=data_string)
