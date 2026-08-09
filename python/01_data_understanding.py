import pandas as pd
from pathlib import Path

# =========================
# 1. DATA PATH
# =========================

DATA_PATH = Path('data/raw')

# =========================
# 2. LOAD DATA
# =========================

datasets = {
    'customers': 'olist_customers_dataset.csv',
    'geolocation': 'olist_geolocation_dataset.csv',
    'order_items': 'olist_order_items_dataset.csv',
    'order_payments': 'olist_order_payments_dataset.csv',
    'order_reviews': 'olist_order_reviews_dataset.csv',
    'orders': 'olist_orders_dataset.csv',
    'products': 'olist_products_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
    'category_translation': 'product_category_name_translation.csv'
}

data = {}

for name, filename in datasets.items():
    filepath = DATA_PATH / filename
    data[name] = pd.read_csv(filepath)

# =========================
# 3. BASIC DATA OVERVIEW
# =========================

for name, df in data.items():
    print('='*60)
    print(f'DATASET: {name}')
    print('='*60)

    print(f'Rows    : {df.shape[0]:,}')
    print(f'Columns : {df.shape[1]}')

    print('\nColumns:')
    print(df.columns.tolist())

    print('\nData Types:')
    print(df.dtypes)

    print('\nMissing Values:')
    print(df.isnull().sum())

    print('\nDuplicate Rows:')
    print(df.duplicated().sum())

    print('\n')