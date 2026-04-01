import sys
import json
import os
from typing import List, Dict, Any

try:
    import pandas as pd
except ImportError:
    pd = None

def parse_file(source: str, file_path: str) -> List[Dict[str, Any]]:
    """
    Parses a CSV or JSON file generically to extract product details.
    You will likely need to adjust the column lookups based on your exact dataset schemas.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    try:
        if file_path.endswith('.csv'):
            if pd is None:
                raise ImportError("Pandas is required to read CSV files.")
            df = pd.read_csv(file_path)
            rows = [row.to_dict() for _, row in df.iterrows()]
        elif file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'items' in data:
                    rows = data['items']
                elif isinstance(data, dict) and 'products' in data:
                    rows = data['products']
                elif isinstance(data, list):
                    rows = data
                else:
                    rows = [data]
        else:
            print("Unsupported file format. Use .json or .csv")
            return []
            
        products = []
        for row in rows:
            # Customize these generic fetchers for your specific file formats
            product_id = str(row.get('id', row.get('product_id', row.get('_id', 'unknown'))))
            name = str(row.get('title', row.get('name', 'unknown')))
            brand = str(row.get('brand', row.get('designer', 'Unknown')))
            category = str(row.get('category', row.get('type', 'Unknown')))
            price_raw = row.get('price', row.get('current_price', 0.0))
            
            try:
                price = float(str(price_raw).replace('$', '').replace(',', ''))
            except (ValueError, TypeError):
                price = 0.0

            currency = str(row.get('currency', 'USD'))

            if product_id != 'unknown':
                products.append({
                    "source": source,
                    "source_product_id": product_id,
                    "name": name,
                    "brand": brand,
                    "category": category,
                    "current_price": price,
                    "currency": currency
                })
                
        return products
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return []
