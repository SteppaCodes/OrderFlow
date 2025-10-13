from .manager import _publisher 

def publish_order_placed(order, product):
    event_data = {
        'order_id': str(order.id),
        'user_id': str(order.user_id),
        'product_id': str(order.product_id),
        'product_name': product['name'],
        'quantity': order.quantity,
        'total_price': str(order.total_price)
    }
    message = {"event": "order.placed", "data": event_data}

    _publisher.publish_event(exchange="orders", routing_key="order.placed", message=message)

def publish_order_confirmed(order):
    event_data = {
        "order_id": str(order.id),
        "product_id": str(order.product_id),
        "quantity": order.quantity
    }

    message = {"event":"order.confirmed", "data": event_data}
    _publisher.publish_event(exchange="orders", routing_key="order.confirmed", message=message)
