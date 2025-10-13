
from ...models import Product
from ..publishers import publish_stock_reserved
from django.db import transaction

def handle_order_placed(data):
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    order_id = data.get('order_id')
    
    try:
        with transaction.atomic():
            product = Product.objects.select_for_update().get(id=product_id)

            if product.stock >= quantity:
                product.stock -= quantity
                product.reserved_stock += quantity
                product.save()

                publish_stock_reserved(product, str(order_id))
                print(f"Reserved {quantity} of product {product_id} for order {order_id}")
            else:
                print(f"Insufficient stock for product {product_id}")
    except Product.DoesNotExist:
        print(f"Product {product_id} not found")
    except Exception as e:
        print(f"Error reserving stock for order {order_id}: {e}")


def handle_order_confirmed(data):
    """
    Consume order.confirmed event issued by order service and update the order service
    """
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    try:
        # Reduce product stock
        with transaction.atomic():
            product = Product.objects.select_for_update().get(id=product_id)
            if product.reserved_stock >= quantity:
                product.reserved_stock -= quantity
                product.save()
                print(f"Confirmed order for product {product_id}, reduced reserved stock by {quantity}")
            else:
                print(f"Insufficient reserved stock for product {product_id} to confirm order")
    except Product.DoesNotExist:
        print(f"Product {product_id} not found")

