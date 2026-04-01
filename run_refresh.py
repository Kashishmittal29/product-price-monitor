import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.services.fetcher import refresh_data_job

if __name__ == "__main__":
    refresh_data_job()
    print("Sync Refresh Job Complete.")
