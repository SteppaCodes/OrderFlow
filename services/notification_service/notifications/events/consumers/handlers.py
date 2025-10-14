

def handle_order_confirmed(data):
    buyer_email = data.get("buyer_email")
    order_id = data.get("order_id")
    product_name = data.get("product_name")
    seller_email = data.get("seller_email")
    amount = data.get("total_price")
    quantity = data.get("quantity")

    email_to_buyer= f"""
    To: {buyer_email}
    Subject: Order Confirmation - Order #{order_id}

    Dear Customer,
    Thank you for your purchase! Your order #{order_id} has been confirmed.
    Amount: ${amount}
    =========================================
    {product_name}: x{quantity}
    We will notify you once your order is shipped.
    Best regards,
    OrderFlow Team
    """

    email_to_seller = f"""
    To: {seller_email}
    Subject: New Order Received! - Order #{order_id}
    Dear Seller,
    You have a new order #{order_id} for {quantity} {product_name} that has been confirmed.
    Amount: ${amount}
    Visit your dashboard to get all information concerning the order and please prepare the item for shipping."""

    # Simulate sending emails by printing to console
    print("Sending email to buyer:")
    print(email_to_buyer)
    print("Sending email to seller:")
    print(email_to_seller)

    print("Emails sent successfully.")