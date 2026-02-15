import json
import logging

from backend.services.chatbot_engine import get_response
from backend.services.conversation_store import (
    add_message,
    create_conversation,
    get_conversation,
)
from backend.utils.response import bad_request, server_error, success

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
    except (json.JSONDecodeError, TypeError):
        return bad_request("Invalid JSON body")

    message = body.get("message", "").strip()
    if not message:
        return bad_request("'message' field is required")

    conversation_id = body.get("conversation_id")

    try:
        # 대화가 없으면 새로 생성
        if not conversation_id:
            conversation = create_conversation()
            conversation_id = conversation["conversation_id"]
        else:
            existing = get_conversation(conversation_id)
            if not existing:
                conversation = create_conversation()
                conversation_id = conversation["conversation_id"]

        # 사용자 메시지 저장
        user_msg = add_message(conversation_id, "user", message)

        # 봇 응답 생성
        bot_reply = get_response(message)

        # 봇 응답 저장
        bot_msg = add_message(conversation_id, "bot", bot_reply)

        return success({
            "conversation_id": conversation_id,
            "user_message": user_msg,
            "bot_message": bot_msg,
        })

    except Exception as e:
        logger.error(f"Chat handler error: {e}")
        return server_error("메시지 처리 중 오류가 발생했습니다.")
