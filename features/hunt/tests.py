from unittest.mock import Mock, patch

import requests
from django.test import TestCase

from .services.api import TibiaDataAPI


class TibiaDataAPITests(TestCase):
    def setUp(self) -> None:
        self.api = TibiaDataAPI()

    @patch("features.hunt.services.api.requests.get")
    def test_get_creatures_uses_v5_and_returns_json(self, get):
        response = Mock(status_code=200)
        response.json.return_value = {"creatures": []}
        get.return_value = response

        result = self.api.get_creatures()

        get.assert_called_once_with("https://api.tibiadata.com/v5/creatures/")
        self.assertEqual(result, {"creatures": []})

    @patch("features.hunt.services.api.requests.get")
    def test_missing_creature_returns_none(self, get):
        get.return_value = Mock(status_code=404)

        self.assertIsNone(self.api.get_especific_creature("unknown"))

    @patch("features.hunt.services.api.requests.get")
    def test_upstream_errors_are_raised(self, get):
        response = Mock(status_code=502)
        response.raise_for_status.side_effect = requests.HTTPError("502 Server Error")
        get.return_value = response

        with self.assertRaises(requests.HTTPError):
            self.api.get_creatures()
