from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.db.database import get_db
from app.db import schemas, models
from app.core.security import get_api_key
from app.services.fetcher import refresh_data_job

router = APIRouter()

@router.get("/products", response_model=List[schemas.ProductResponse])
def get_products(
    category: Optional[str] = None,
    source: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    if category:
        query = query.filter(models.Product.category.ilike(f"%{category}%"))
    if source:
        query = query.filter(models.Product.source == source)
    if min_price is not None:
        query = query.filter(models.Product.current_price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.current_price <= max_price)
        
    return query.offset(offset).limit(limit).all()

@router.get("/products/{product_id}", response_model=schemas.ProductDetailResponse)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/analytics/overview")
def get_analytics(db: Session = Depends(get_db)):
    total_products = db.query(models.Product).count()
    sources_records = db.query(models.Product.source).distinct().all()
    sources = [s[0] for s in sources_records if s[0]]
    
    avg_price_per_category = db.query(
        models.Product.category,
        func.avg(models.Product.current_price)
    ).group_by(models.Product.category).all()

    avg_prices = [{"category": row[0], "avg_price": round(row[1], 2)} for row in avg_price_per_category if row[0]]

    return {
        "total_products": total_products,
        "sources": sources,
        "avg_prices": avg_prices
    }

@router.post("/jobs/refresh", status_code=202)
def trigger_refresh(background_tasks: BackgroundTasks, api_key: str = Depends(get_api_key)):
    """Triggers an async background job to parse data files locally based on DB requirements."""
    background_tasks.add_task(refresh_data_job)
    return {"message": "Data refresh job started. Ensure CSV/JSON files are present in the 'data' directory."}
