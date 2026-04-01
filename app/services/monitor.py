from sqlalchemy.orm import Session
from app.db.models import Product, PriceHistory
from app.services.notifications import notify_price_change
import hashlib
from datetime import datetime

def process_product_data(db: Session, data: dict):
    source = data["source"]
    source_id = data["source_product_id"]
    
    product = db.query(Product).filter(
        Product.source == source,
        Product.source_product_id == source_id
    ).first()

    if not product:
        # Generate a stable ID
        unique_string = f"{source}-{source_id}"
        prod_id = hashlib.sha256(unique_string.encode()).hexdigest()
        
        product = Product(
            id=prod_id,
            source=source,
            source_product_id=source_id,
            name=data["name"],
            brand=data["brand"],
            category=data["category"],
            current_price=data["current_price"],
            currency=data["currency"],
            last_updated=datetime.utcnow()
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        
        # Initial price history setup
        history = PriceHistory(product_id=product.id, price=data["current_price"])
        db.add(history)
        db.commit()
    else:
        # Update last seen timestamp
        product.last_updated = datetime.utcnow()
        db.commit()
        
        # Check if price changed
        if abs(product.current_price - data["current_price"]) > 0.01:
            old_price = product.current_price
            new_price = data["current_price"]
            
            product.current_price = new_price
            db.commit()
            
            history = PriceHistory(product_id=product.id, price=new_price)
            db.add(history)
            db.commit()
            
            # Trigger notification
            notify_price_change(product, old_price, new_price)
