from orders.models import Order
from ..publisher import publish_order_confirmed

def handle_payment_successful(data):
    order_id = data.get("order_id")

    try:
        order = Order.objects.get(id=order_id)
        order.status = "paid"
        order.save()
        publish_order_confirmed(order)
        print(f"Order {order_id} marked as paid.")

    except Order.DoesNotExist:
        print(f"Order with id {order_id} does not exist.")
        return