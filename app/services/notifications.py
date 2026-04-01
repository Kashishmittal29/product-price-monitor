import logging
from app.db.models import Product

logger = logging.getLogger(__name__)

def notify_price_change(product: Product, old_price: float, new_price: float):
    # Here you could implement a webhook dispatch, e.g., requests.post(webhook_url, json=...)
    # We use basic logging for standard tracking
    if new_price < old_price:
        logger.warning(f"PRICE DROP! {product.name} ({product.source}) dropped from ${old_price} to ${new_price}")
    else:
        logger.warning(f"PRICE INCREASE! {product.name} ({product.source}) went from ${old_price} to ${new_price}")
