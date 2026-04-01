from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True)
    source = Column(String, index=True)
    source_product_id = Column(String, index=True)
    name = Column(String)
    brand = Column(String, index=True)
    category = Column(String, index=True)
    current_price = Column(Float)
    currency = Column(String, default="USD")
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan", order_by="desc(PriceHistory.timestamp)")

    __table_args__ = (UniqueConstraint('source', 'source_product_id', name='_source_source_id_uc'),)

class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"), index=True)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="price_history")
