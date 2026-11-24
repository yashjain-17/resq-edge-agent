import unittest
from unittest.mock import Mock, patch

from fastapi import HTTPException

from agent.server import QueryRequest, health_check, query_agent


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


class QueryAgentResponseTests(unittest.TestCase):
    @patch("agent.server.requests.post")
    def test_rejects_non_object_model_payload(self, mock_post):
        response = Mock()
        response.json.return_value = ["unexpected", "list"]
        mock_post.return_value = response

        with self.assertRaises(HTTPException) as context:
            query_agent(QueryRequest(prompt="Assess the telemetry"))

        self.assertEqual(context.exception.status_code, 502)
        self.assertEqual(
            context.exception.detail,
            "The local model returned an invalid response payload.",
        )

    @patch("agent.server.requests.post")
    def test_rejects_non_string_model_response(self, mock_post):
        response = Mock()
        response.json.return_value = {"response": {"text": "not a string"}}
        mock_post.return_value = response

        with self.assertRaises(HTTPException) as context:
            query_agent(QueryRequest(prompt="Assess the telemetry"))

        self.assertEqual(context.exception.status_code, 502)

    @patch("agent.server.requests.post")
    def test_trims_valid_model_response(self, mock_post):
        response = Mock()
        response.json.return_value = {"response": "  Check battery level.  "}
        mock_post.return_value = response

        result = query_agent(QueryRequest(prompt="Assess the telemetry"))

        self.assertEqual(result["response"], "Check battery level.")
        self.assertEqual(result["status"], "generated")


if __name__ == "__main__":
    unittest.main()
