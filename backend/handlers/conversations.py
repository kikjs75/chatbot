import logging

from backend.services.conversation_store import get_conversation, list_conversations
from backend.utils.response import not_found, server_error, success

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def list_handler(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        limit = int(params.get("limit", 20))
        conversations = list_conversations(limit=limit)
        return success({"conversations": conversations})
    except Exception as e:
        logger.error(f"List conversations error: {e}")
        return server_error("대화 목록 조회 중 오류가 발생했습니다.")


def get_handler(event, context):
    try:
        conversation_id = event["pathParameters"]["id"]
        conversation = get_conversation(conversation_id)
        if not conversation:
            return not_found("대화를 찾을 수 없습니다.")
        return success({"conversation": conversation})
    except Exception as e:
        logger.error(f"Get conversation error: {e}")
        return server_error("대화 조회 중 오류가 발생했습니다.")
