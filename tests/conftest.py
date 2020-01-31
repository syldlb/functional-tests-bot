import pytest
import json


@pytest.fixture
def giphy_search_response():
    with open("tests/giphy_search.json") as json_file:
        mock_json = json.load(json_file)
    return mock_json
