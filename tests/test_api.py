import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import warnings

from app.main import app
from app.db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Price Monitor API"}

def test_trigger_refresh_unauthorized():
    response = client.post("/api/v1/jobs/refresh")
    assert response.status_code == 401

def test_trigger_refresh_authorized():
    response = client.post("/api/v1/jobs/refresh", headers={"X-API-Key": "secret-token-123"})
    assert response.status_code == 202

def test_get_analytics_empty():
    response = client.get("/api/v1/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["total_products"] == 0
    assert data["sources"] == []
    assert data["avg_prices"] == []
