import unittest
from unittest.mock import Mock, patch

from agent.server import health_check


class HealthCheckTests(unittest.TestCase):
    @patch("agent.server.requests.get")
    def test_reports_configured_model_when_tags_are_valid(self, mock_get):
        response = Mock()
        response.json.return_value = {"models": [{"name": "gemma2:9b"}]}
        mock_get.return_value = response

        result = health_check()

        self.assertEqual(result["status"], "online")
        self.assertTrue(result["model_available"])

    @patch("agent.server.requests.get")
    def test_malformed_model_payload_is_reported_as_offline(self, mock_get):
        response = Mock()
        response.json.return_value = ["not", "an", "object"]
        mock_get.return_value = response

        result = health_check()

        self.assertEqual(result["status"], "offline")
        self.assertFalse(result["model_available"])

    @patch("agent.server.requests.get")
    def test_invalid_model_entries_do_not_crash_health_check(self, mock_get):
        response = Mock()
        response.json.return_value = {"models": [None, "invalid", {"name": "other"}]}
        mock_get.return_value = response

        result = health_check()

        self.assertEqual(result["status"], "online")
        self.assertFalse(result["model_available"])


if __name__ == "__main__":
    unittest.main()
