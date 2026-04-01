import os
import asyncio
from app.services.parser import parse_file
from app.services.monitor import process_product_data
from app.db.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

def refresh_data_job():
    """
    Simulates an async background task parsing files from the 'data' directory.
    When users upload JSON or CSV to the 'data' folder, this logic will pick it up
    and ingest/update.
    """
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logger.info(f"Created {data_dir} directory. Add your JSON/CSV files there.")
        return
        
    db = SessionLocal()
    try:
        files = []
        for root, _, filenames in os.walk(data_dir):
            for filename in filenames:
                if filename.endswith(('.json', '.csv')):
                    files.append(os.path.join(root, filename))
                    
        if not files:
            logger.info("No files found in data directory.")
            return

        for file_path in files:
            filename = os.path.basename(file_path)
            
            # Simple heuristic for source based on filename
            source = "unknown"
            if "grailed" in filename.lower(): source = "grailed"
            elif "fashionphile" in filename.lower(): source = "fashionphile"
            elif "1stdibs" in filename.lower(): source = "1stdibs"
            else: source = "custom"
            
            logger.info(f"Parsing file {filename} as source: {source}")
            parsed_data = parse_file(source, file_path)
            if not parsed_data:
                continue

            for item in parsed_data:
                process_product_data(db, item)
            
            logger.info(f"Finished processing {len(parsed_data)} items from {filename}")
                
    except Exception as e:
        logger.error(f"Error during refresh job: {e}")
    finally:
        db.close()
