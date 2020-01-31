import json
from unittest.mock import patch
from bot.slack import post_on_slack


def test_post_on_slack():
    with patch("bot.slack.requests.post") as mock_post:
        post_on_slack(
            "http://fake-jenkins.org/",
            "http://fake-hook.org",
            "fake-job",
            "Fake message",
            "fake-color",
            "http://fake-gif.org",
        )
        attachments = {
            "attachments": [
                {
                    "fallback": "Fake message",
                    "color": "fake-color",
                    "title": "fake-job",
                    "title_link": "http://fake-jenkins.org/job/fake-job",
                    "text": "Fake message",
                    "image_url": "http://fake-gif.org",
                }
            ]
        }
        mock_post.assert_called_once_with(
            "http://fake-hook.org", data=json.dumps(attachments)
        )


def test_post_on_slack_no_gif():
    pass
