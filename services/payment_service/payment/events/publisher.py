from .manager import _publisher

def publish_payment_successful(payment_data):
    event_data = {
        "payment_id": payment_data["id"],
        "order_id": payment_data["order_id"],
    }
    message = {"event":"payment.successful", "data": event_data}

    _publisher.publish_event(exchange="payment", routing_key="payment.successful", message=message)
