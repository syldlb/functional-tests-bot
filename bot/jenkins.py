from bot.helpers import auth_get


def get_tests_list(jenkins_url, job_name, user, password):
    project_url = f"{jenkins_url}job/{job_name}/lastBuild/api/json"
    project_response = auth_get(project_url, user, password)
    print("response code: %s" % project_response.status_code)
    return project_response


def get_run_detail_response(run_url, user, password):
    run_detail_url = run_url + "api/json"
    run_detail_response = auth_get(run_detail_url, user, password)
    return run_detail_response
