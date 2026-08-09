import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

RAW_PATH = Path('data/raw')
PROCESSED_PATH = Path('data/processed')

PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

# ============================================================
# HELPER FUNCTIONS 
# ============================================================

def load_dataset(filename):
    """Load CSV dataset from raw data folder."""
    return pd.read_csv(RAW_PATH / filename)

def save_dataset(df, filename):
    """Save cleaned dataset to processed data folder."""
    df.to_csv(PROCESSED_PATH / filename, index=False)
    print(f'Saved: {filename} | Rows: {len(df):,}')

# ============================================================
# 1. CLEAN ORDERS
# ============================================================

print('\n' + '=' * 60)
print('CLEANING: ORDERS')
print('=' * 60)

orders = load_dataset('olist_orders_dataset.csv')

# Convert timestamp columns from string to datetime
date_columns = [
    "order_purchase_timestamp",
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]

for column in date_columns:
    orders[column] = pd.to_datetime(orders[column], errors='coerce')

# Create delivery time in days
orders['delivery_days'] = (
    orders['order_delivered_customer_date']
    - orders['order_purchase_timestamp']
).dt.total_seconds() / (24 * 60 * 60)

# Create estimated delivery delay
orders['delivery_delay_days'] = (
    orders['order_delivered_customer_date']
    - orders['order_estimated_delivery_date']
).dt.total_seconds() / (24*60*60)

# Keep valid delivery times
orders.loc[orders['delivery_days'] < 0, 'delivery_days'] = pd.NA

save_dataset(orders, 'orders_cleaned.csv')

# ============================================================
# 2. CLEAN PRODUCTS
# ============================================================

print('\n' + '=' * 60)
print('CLEANING: PRODUCTS')
print('=' * 60)

products = load_dataset('olist_products_dataset.csv')

# Missing product category
products['product_category_name'] = (
    products['product_category_name']
    .fillna('unknown')
)

# Numeric product attributes
numeric_columns = [
    'product_name_lenght',
    'product_description_lenght',
    'product_photos_qty',
    'product_weight_g',
    'product_length_cm',
    'product_height_cm',
    'product_width_cm'
]

# Fiil missing numeric values with median
for column in numeric_columns:
    products[column] = products[column].fillna(
        products[column].median()
    )

save_dataset(products, 'products_cleaned.csv')

# ============================================================
# 3. CLEAN ORDER REVIEWS
# ============================================================

print('n' + '=' * 60)
print('CLEANING: ORDER REVIEWS')
print('=' * 60)

reviews = load_dataset('olist_order_reviews_dataset.csv')

# Convert dates
review_date_columns = [
    'review_creation_date',
    'review_answer_timestamp'
]

for column in review_date_columns:
    reviews[column] = pd.to_datetime(
        reviews[column],
        errors='coerce'
    )

# Missing review titles/messages do not mean missing reviews.
# They mean the customer did not provide text.
reviews['review_comment_title'] = (
    reviews['review_comment_title']
    .fillna('')
)

reviews['review_comment_message'] = (
    reviews['review_comment_message']
    .fillna('')
)

# Create indicator for whether customer left a written comment
reviews['has_comment'] = (
    reviews['review_comment_message'].str.strip() != ''
)

save_dataset(reviews, 'order_reviews_cleaned.csv')

# ============================================================
# 4. CLEAN GEOLOCATION
# ============================================================

print('\n' + '=' * 60)
print('CLEANING: GEOLOCATION')
print('=' * 60)

geolocation = load_dataset('olist_geolocation_dataset.csv')

# Remove exact duplicate rows
geolocation = geolocation.drop_duplicates()

save_dataset(geolocation, 'geolocation_cleaned.csv')

# ============================================================
# SUMMARY
# ============================================================

print('\n' + '=' * 60)
print('DATA CLEANING COMPLETED')
print('=' * 60)

print(f'Processed files saved to: {PROCESSED_PATH}')