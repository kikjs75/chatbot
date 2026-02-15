from backend.utils.response import success


def handler(event, context):
    return success({
        "status": "healthy",
        "service": "customer-chatbot",
    })
