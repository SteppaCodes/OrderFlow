from .manager import _publisher

def publish_user_created(user):
    message = {
        "event": "user.created",
        "data": {
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat(),
        }
    }

    _publisher.publish_event(exchange="users", routing_key="user.created", message=message)