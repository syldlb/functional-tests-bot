from unittest.mock import patch
from bot.jenkins import get_tests_list, get_run_detail_response


def test_get_tests_list():
    with patch("bot.jenkins.auth_get") as mock_get:
        get_tests_list("http://fake-jenkins.org/", "fake_job", "usr", "pwd")
        project_url = "http://fake-jenkins.org/job/fake_job/lastBuild/api/json"
        mock_get.assert_called_once_with(project_url, "usr", "pwd")


def test_get_run_detail_response():
    with patch("bot.jenkins.auth_get") as mock_get:
        get_run_detail_response("http://fake-run.org/", "usr", "pwd")
        mock_get.assert_called_once_with("http://fake-run.org/api/json", "usr", "pwd")
