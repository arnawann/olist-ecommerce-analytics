import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

PROCESSED_PATH = Path('data/processed')

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_dataset(filename):
    '''Load cleaned dataset from processed data folder.'''
    return pd.read_csv(PROCESSED_PATH / filename)

def print_check(label, condition):
    '''Print validation result.'''
    status = 'PASS' if condition else 'FAIL'
    print(f'[{status}] {label}')

# ============================================================
# 1. VALIDATE ORDERS
# ============================================================

print('\n' + '=' * 60)
print('VALIDATING: ORDERS')
print('=' * 60)

orders = load_dataset('orders_cleaned.csv')

# Row count
print_check(
    'Orders row count preserved',
    len(orders) == 99_441
)

# Check date columns
date_columns = [
    'order_purchase_timestamp',
    'order_approved_at',
    'order_delivered_carrier_date',
    'order_delivered_customer_date',
    'order_estimated_delivery_date'
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors='coerce'
    )

    print_check(
        f'{column} converted to datetime',
        pd.api.types.is_datetime64_any_dtype(orders[column])
    )

# Check delivery days
negative_delivery_days = (
    orders['delivery_days'].dropna() < 0
).sum()

print_check(
    'No negative delivery days',
    negative_delivery_days == 0
)

# Check delivery delay calculation
print_check(
    'Delivery delay column exists',
    'delivery_delay_days' in orders.columns
)

# ============================================================
# 2. VALIDATE PRODUCTS
# ============================================================

print('\n' + '=' * 60)
print('VALIDATING: PRODUCTS')
print('=' * 60)

products = load_dataset('products_cleaned.csv')

# Row count
print_check(
    'Products row count preserved',
    len(products) == 32_951
)

# Product category
missing_category = products[
    'product_category_name'
].isna().sum()

print_check(
    'No missing product categories',
    missing_category == 0
)

# Numeric columns
numeric_columns = [
    'product_name_lenght',
    'product_description_lenght',
    'product_photos_qty',
    'product_weight_g',
    'product_length_cm',
    'product_height_cm',
    'product_width_cm'
]

for column in numeric_columns:

    missing_values = products[column].isna().sum()

    print_check(
        f'No missing values in {column}',
        missing_values == 0
    )

# ============================================================
# 3. VALIDATE ORDER REVIEWS
# ============================================================

print('\n' + '=' * 60)
print('VALIDATING: ORDER REVIEWS')
print('=' * 60)

reviews = load_dataset('order_reviews_cleaned.csv')

# Row count
print_check(
    'No missing review messages',
    reviews['review_comment_message'].isna().sum() == 0
)

print_check(
    "No missing review titles",
    reviews['review_comment_title'].isna().sum() == 0
)

# has_comment column
print_check(
    'has_comment column exists',
    'has_comment' in reviews.columns
)

# Check has_comment values
valid_has_comment_values = (
    reviews['has_comment']
    .dropna()
    .isin([True, False])
    .all()
)

print_check(
    'has_comment contains only True/False',
    valid_has_comment_values
)

# ============================================================
# 4. VALIDATE GEOLOCATION
# ============================================================

print('\n' + '=' * 60)
print('VALIDATING: GEOLOCATION')
print('=' * 60)

geolocation = load_dataset('geolocation_cleaned.csv')

duplicate_rows = geolocation.duplicated().sum()

print_check(
    'No duplicate rows',
    duplicate_rows == 0
)

print(f'Geolocation rows after cleaning: {len(geolocation):,}')

# ============================================================
# SUMMARY
# ============================================================

print('\n' + '=' * 60)
print('DATA VALIDATION COMPLETED')
print('=' * 60)

print('All validation checks have been executed.')