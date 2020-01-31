from unittest.mock import patch, Mock
from bot.giphy import get_random_gif_url


def test_get_random_gif_url(giphy_search_response):
    with patch("bot.giphy.requests.get") as mock_get:
        mock_resp = Mock()
        mock_resp.json = Mock()
        mock_resp.json.return_value = giphy_search_response
        mock_get.return_value = mock_resp
        url = get_random_gif_url("mock_category", "fake_key")
        mock_get.assert_called_once_with(
            "https://api.giphy.com/v1/gifs/search",
            {"api_key": "fake_key", "q": "mock_category", "rating": "g"},
        )
        assert "giphy.com" in url
        assert ".gif" in url
