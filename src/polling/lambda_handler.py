from src.polling.poller import poll


def handler(event, context):
    try:
        result = poll()
        return {"status": "success", "message": result["message"]}
    except Exception as e:
        return {"status": "failure", "message": str(e)}