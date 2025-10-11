
from .manager import _publisher

def publish_stock_updated(product):
    message = {
        "event": "product.stock_updated",
        "data": {
            "product_id": product.id,
            "new_stock": product.stock,
        }
    }

    _publisher.publish_event(exchange="products", routing_key="stock.updated", message=message)

def publish_stock_reserved(product, order_id):
    message = {
        "event": "product.stock_reserved",
        "data": {
            "product_id": str(product.id),
            "reserved_stock": product.reserved_stock,
            "order_id": str(order_id)
        }
    }

    _publisher.publish_event(exchange="products", routing_key="stock.reserved", message=message)