import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

RAW_PATH = Path('data/raw')
PROCESSED_PATH = Path('data/processed')
ANALYTICS_PATH = Path('data/analytics')

ANALYTICS_PATH.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_dataset(filename, folder):
    """Load dataset from specified folder."""
    return pd.read_csv(folder / filename)


def save_dataset(df, filename):
    """Save analytical dataset."""
    df.to_csv(ANALYTICS_PATH / filename, index=False)

    print(
        f'Saved: {filename} | '
        f'Rows: {len(df):,} | '
        f'Columns: {len(df.columns)}'
    )


# ============================================================
# LOAD DATASETS
# ============================================================

print('\n' + '=' * 60)
print('LOADING DATASETS')
print('=' * 60)

orders = load_dataset(
    'orders_cleaned.csv',
    PROCESSED_PATH
)
customers = load_dataset(
    'olist_customers_dataset.csv',
    RAW_PATH
)
order_items = load_dataset(
    'olist_order_items_dataset.csv',
    RAW_PATH
)
order_payments = load_dataset(
    'olist_order_payments_dataset.csv',
    RAW_PATH
)
order_reviews = load_dataset(
    'order_reviews_cleaned.csv',
    PROCESSED_PATH
)

# ============================================================
# PREPARE ORDERS
# ============================================================

print('\n' + '=' * 60)
print('TRANSFORMING ORDERS')
print('=' * 60)

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


# ============================================================
# AGGREGATE ORDER ITEMS
# ============================================================

print('\n' + '=' * 60)
print('AGGREGATING ORDER ITEMS')
print('=' * 60)

order_items_summary = (
    order_items
    .groupby('order_id')
    .agg(
        total_items=('order_item_id', 'count'),
        total_product_price=('price', 'sum'),
        total_freight_value=('freight_value', 'sum')
    )
    .reset_index()
)


# ============================================================
# AGGREGATE PAYMENTS
# ============================================================

print('\n' + '=' * 60)
print('AGGREGATING PAYMENTS')
print('=' * 60)

payment_summary = (
    order_payments
    .groupby('order_id')
    .agg(
        total_payment_value=('payment_value', 'sum'),
        payment_installments=('payment_installments', 'max')
    )
    .reset_index()
)


# ============================================================
# AGGREGATE REVIEWS
# ============================================================

print('\n' + '=' * 60)
print('AGGREGATING REVIEWS')
print('=' * 60)

review_summary = (
    order_reviews
    .groupby('order_id')
    .agg(
        review_score=('review_score', 'mean'),
        has_comment=('has_comment', 'max')
    )
    .reset_index()
)

# ============================================================
# MERGE ORDER-LEVEL DATA
# ============================================================

print('\n' + '=' * 60)
print('MERGING ORDER-LEVEL DATA')
print('=' * 60)

order_analysis = (
    orders
    .merge(
        customers,
        on='customer_id',
        how='left'
    )
    .merge(
        order_items_summary,
        on='order_id',
        how='left'
    )
    .merge(
        payment_summary,
        on='order_id',
        how='left'
    )
    .merge(
        review_summary,
        on='order_id',
        how='left'
    )
)


# ============================================================
# CREATE BUSINESS METRICS
# ============================================================

print('\n' + '=' * 60)
print('CREATING BUSINESS METRICS')
print('=' * 60)

# Total order value
order_analysis['total_order_value'] = (
    order_analysis['total_product_price'].fillna(0)
    + order_analysis['total_freight_value'].fillna(0)
)


# Delivery status
order_analysis['delivery_status'] = 'Not Delivered'

order_analysis.loc[
    order_analysis['order_delivered_customer_date'].notna(),
    'delivery_status'
] = 'Delivered'


# Delivery performance
order_analysis['delivery_performance'] = 'Unknown'

order_analysis.loc[
    order_analysis['delivery_delay_days'] < 0,
    'delivery_performance'
] = 'Early'

order_analysis.loc[
    order_analysis['delivery_delay_days'] == 0,
    'delivery_performance'
] = 'On Time'

order_analysis.loc[
    order_analysis['delivery_delay_days'] > 0,
    'delivery_performance'
] = 'Late'


# ============================================================
# SAVE
# ============================================================

save_dataset(
    order_analysis,
    'order_analysis.csv'
)


# ============================================================
# SUMMARY
# ============================================================

print('\n' + '=' * 60)
print('DATA TRANSFORMATION COMPLETED')
print('=' * 60)

print(
    f'Order-level analytical dataset created: '
    f'{len(order_analysis):,} rows'
)