from src.polling.poller import poll


def handler(event, context):
    try:
        poll()
        success_message = "Polling completed successfully"
        return {"status": "success", "message": success_message}
    except Exception as e:
        error_message = f"Polling failed: {str(e)}"
        return {"status": "failure", "message": error_message}

