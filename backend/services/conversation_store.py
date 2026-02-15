import os
import uuid
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Key


TABLE_NAME = os.environ.get("CONVERSATIONS_TABLE", "customer-chatbot-conversations-dev")


def _get_table():
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(TABLE_NAME)


def create_conversation():
    table = _get_table()
    conversation_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    item = {
        "conversation_id": conversation_id,
        "created_at": now,
        "updated_at": now,
        "messages": [],
    }
    table.put_item(Item=item)
    return item


def add_message(conversation_id, role, content):
    table = _get_table()
    now = datetime.now(timezone.utc).isoformat()
    message = {
        "role": role,
        "content": content,
        "timestamp": now,
    }
    table.update_item(
        Key={"conversation_id": conversation_id},
        UpdateExpression="SET messages = list_append(if_not_exists(messages, :empty), :msg), updated_at = :now",
        ExpressionAttributeValues={
            ":msg": [message],
            ":empty": [],
            ":now": now,
        },
    )
    return message


def get_conversation(conversation_id):
    table = _get_table()
    response = table.get_item(Key={"conversation_id": conversation_id})
    return response.get("Item")


def list_conversations(limit=20):
    table = _get_table()
    response = table.scan(
        ProjectionExpression="conversation_id, created_at, updated_at",
        Limit=limit,
    )
    items = response.get("Items", [])
    items.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    return items
