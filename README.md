# Product Price Monitoring System

A comprehensive system to monitor product prices over time, parse different source datasets (like Grailed, Fashionphile, 1stdibs), and log price histories using a cleanly architected FastAPI backend. 

## Features
- **FastAPI Backend**: Clean and extensible REST APIs.
- **Async Data Ingestion**: Pick up and parse large JSON/CSV files dynamically.
- **Price History Tracking**: Monitor changes intelligently and push notifications (logged warnings).
- **SQLite Database**: SQLAlchemy based simple local database.

## System Setup

1. **Backend**:
   ```bash
   python -m venv venv
   # activate the environment
   pip install -r requirements.txt
   ```

2. **Frontend UI**:
   - Navigate to `frontend` directory.
   - Run `npm install` and `npm run dev`.

## Ingesting Data

1. Place your exported JSON or CSV files into the `data/` directory (e.g., `data/grailed.json`, `data/fashionphile.csv`).
2. Start the API using `uvicorn app.main:app --reload`
3. Hit the trigger endpoint to start parsing and ingestion:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/jobs/refresh" -H "X-API-Key: secret-token-123"
   ```

## Design Decisions

- **Price History Scales**: Using a one-to-many relationship with indexed `product_id`. Data is normalized and we only store when the price actually changes. 
- **Notification approach**: Currently stubbed as Python standard library `logging` levels for simplicity, but abstracted behind `notify_price_change()` for easy drop-in with Discord/Slack webhooks.
- **Handling 100+ sources**: The `app.services.parser` utilizes generalized processing functions. It's meant to be modified for custom adapters based on source.

## Testing

```bash
pytest tests/
```
