def on_message(message, receipts):
    return receipts.deliver(message.order_id, message.address)
