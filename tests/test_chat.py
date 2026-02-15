import json
from unittest.mock import MagicMock, patch

import pytest

from backend.handlers.chat import handler


@pytest.fixture
def mock_dynamo():
    with patch("backend.handlers.chat.create_conversation") as mock_create, \
         patch("backend.handlers.chat.get_conversation") as mock_get, \
         patch("backend.handlers.chat.add_message") as mock_add:
        mock_create.return_value = {
            "conversation_id": "test-conv-id",
            "created_at": "2024-01-01T00:00:00+00:00",
            "updated_at": "2024-01-01T00:00:00+00:00",
            "messages": [],
        }
        mock_get.return_value = {
            "conversation_id": "test-conv-id",
            "messages": [],
        }
        mock_add.side_effect = lambda cid, role, content: {
            "role": role,
            "content": content,
            "timestamp": "2024-01-01T00:00:00+00:00",
        }
        yield {"create": mock_create, "get": mock_get, "add": mock_add}


class TestChatHandler:
    def test_new_conversation(self, mock_dynamo):
        event = {"body": json.dumps({"message": "안녕하세요"})}
        result = handler(event, None)
        body = json.loads(result["body"])

        assert result["statusCode"] == 200
        assert body["conversation_id"] == "test-conv-id"
        assert body["bot_message"]["role"] == "bot"
        mock_dynamo["create"].assert_called_once()

    def test_existing_conversation(self, mock_dynamo):
        event = {"body": json.dumps({"message": "배송 문의", "conversation_id": "test-conv-id"})}
        result = handler(event, None)
        body = json.loads(result["body"])

        assert result["statusCode"] == 200
        assert body["conversation_id"] == "test-conv-id"
        mock_dynamo["create"].assert_not_called()

    def test_missing_message(self, mock_dynamo):
        event = {"body": json.dumps({})}
        result = handler(event, None)

        assert result["statusCode"] == 400

    def test_empty_message(self, mock_dynamo):
        event = {"body": json.dumps({"message": "  "})}
        result = handler(event, None)

        assert result["statusCode"] == 400

    def test_invalid_json(self, mock_dynamo):
        event = {"body": "not json"}
        result = handler(event, None)

        assert result["statusCode"] == 400

    def test_no_body(self, mock_dynamo):
        event = {"body": None}
        result = handler(event, None)

        assert result["statusCode"] == 400

    def test_cors_headers(self, mock_dynamo):
        event = {"body": json.dumps({"message": "hello"})}
        result = handler(event, None)

        assert result["headers"]["Access-Control-Allow-Origin"] == "*"

    def test_bot_response_saved(self, mock_dynamo):
        event = {"body": json.dumps({"message": "배송 문의"})}
        handler(event, None)

        calls = mock_dynamo["add"].call_args_list
        assert len(calls) == 2
        assert calls[0][0][1] == "user"
        assert calls[1][0][1] == "bot"
