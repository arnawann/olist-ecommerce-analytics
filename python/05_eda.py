import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

ANALYTICS_PATH = Path('data/analytics')

OUTPUT_PATH = Path('outputs/eda')

OUTPUT_PATH.mkdir(
    parents=True,
       exist_ok=True
)

# ============================================================
# LOAD DATA
# ============================================================

print('\n' + '=' * 60)
print('LOADING ANALYTICAL DATA')
print('=' * 60)

df = pd.read_csv(
    ANALYTICS_PATH / 'order_analysis.csv'
)

print(f'Rows    : {len(df):,}')
print(f'Columns : {len(df.columns)}')

# ============================================================
# PREPARATION
# ============================================================

df['order_purchase_timestamp'] = pd.to_datetime(
    df['order_purchase_timestamp'],
    errors='coerce'
)

df['purchase_month'] = (
    df['order_purchase_timestamp']
    .dt.to_period('M')
    .astype(str)
)

# ============================================================
# EDA 1 — SALES PERFORMANCE
# ============================================================

print('\n' + '=' * 60)
print('EDA 1 - SALES PERFORMANCE')
print('=' * 60)

total_orders = df['order_id'].nunique()

total_revenue = (
    df['total_order_value']
    .sum()
)

average_order_value = (
    df['total_order_value']
    .mean()
)

print(f'Total Orders        : {total_orders:,}')
print(f'Total Revenue       : R$ {total_revenue:,.2f}')
print(f'Average Order Value : R$ {average_order_value:,.2f}')

# Monthly revenue

monthly_sales = (
    df.groupby('purchase_month')
    .agg(
        revenue=('total_order_value', 'sum'),
        orders=('order_id', 'nunique')
    )
    .reset_index()
)

print('\nMonthly Revenue:')
print(monthly_sales.to_string(index=False))

plt.figure(figsize=(10,5))

sns.lineplot(
    data=monthly_sales,
    x='purchase_month',
    y='revenue'
)

plt.title('Monthly Revenue')
plt.xlabel('Month')
plt.ylabel('Revenue (R$)')
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_PATH / '01_monthly_revenue.png',
    dpi=300
)

plt.show()

# ============================================================
# EDA 2 — PRODUCT PERFORMANCE
# ============================================================

print('\n' + '=' * 60)
print('EDA 2 - PRODUCT PERFORMANCE')
print('=' * 60)

# Load order items because product information
# is stored at item level.

order_items = pd.read_csv(
    Path('data/raw') / 'olist_order_items_dataset.csv'
)

products = pd.read_csv(
    Path('data/processed') / 'products_cleaned.csv'
)

category_translation = pd.read_csv(
    Path('data/raw') / 'product_category_name_translation.csv'
)

# Merge product category

product_data = (
    order_items
    .merge(
        products[
            ['product_id', 'product_category_name']
        ],
        on='product_id',
        how='left'
    )
    .merge(
        category_translation,
        on='product_category_name',
        how='left'
    )
)

# Use English category name when available

product_data['category'] = (
    product_data['product_category_name_english']
    .fillna(
        product_data['product_category_name']
    )
    .fillna('Unknown')
)

# Top categories by revenue

category_sales = (
    product_data
    .groupby('category')
    .agg(
        revenue=('price', 'sum'),
        items_sold=('order_item_id', 'count')
    )
    .reset_index()
    .sort_values('revenue', ascending=False)
)

print('\nTop 10 Product Categories by Revenue:')

print(
    category_sales
    .head(10)
    .to_string(index=False)
)

plt.figure(figsize=(10,6))

top_categories = (
    category_sales
    .head(10)
    .sort_values('revenue')
)

plt.barh(
    top_categories['category'],
    top_categories['revenue']
)

plt.title('Top 10 Product Categories by Revenue')
plt.xlabel('Revenue (R$)')
plt.ylabel('Product Category')

plt.tight_layout()

plt.savefig(
    OUTPUT_PATH / '02_top_product_categories.png',
    dpi=300
)

plt.show()

# ============================================================
# EDA 3 — GEOGRAPHICAL PERFORMANCE
# ============================================================

print('\n' + '=' * 60)
print('EDA 3 - GEOGRAPHICAL PERFORMANCE')
print('=' * 60)

state_sales = (
    df.groupby('customer_state')
    .agg(
        orders=('order_id', 'nunique'),
        revenue=('total_order_value', 'sum')
    )
    .reset_index()
    .sort_values(
        'revenue',
        ascending=False
    )
)

print('\nTop 10 States by Revenue:')

print(
    state_sales
    .head(10)
    .to_string(index=False)
)

plt.figure(figsize=(10, 6))

top_states = (
    state_sales
    .head(10)
    .sort_values('revenue')
)

plt.barh(
    top_states['customer_state'],
    top_states['revenue']
)

plt.title(
    'Top 10 States by Revenue'
)

plt.xlabel('Revenue (R$)')
plt.ylabel('State')

plt.tight_layout()

plt.savefig(
    OUTPUT_PATH / '03_top_states_revenue.png',
    dpi=300
)

plt.show()

# ============================================================
# EDA 4 — DELIVERY PERFORMANCE
# ============================================================

print('\n' + '=' * 60)
print('EDA 4 - DELIVERY PERFORMANCE')
print('=' * 60)

delivered_orders = df[
    df['delivery_days'].notna()
].copy()

average_delivery_days = (
    delivered_orders['delivery_days']
    .mean()
)

average_delivery_delay = (
    delivered_orders['delivery_delay_days']
    .mean()
)

print(
    f'Average Delivery Time : '
    f'{average_delivery_days:.2f} days'
)

print(
    f'Average Delivery Delay : '
    f'{average_delivery_delay:.2f} days'
)

delivery_performance = (
    delivered_orders[
        'delivery_performance'
    ]
    .value_counts()
)

print('\nDelivery Performance:')
print(delivery_performance)

plt.figure(figsize=(8,5))

sns.countplot(
    data=delivered_orders,
    x='delivery_performance',
    order=[
        'Early',
        'On Time',
        'Late'
    ]
)

plt.title(
    'Delivery Performance'
)

plt.xlabel('Delivery Performance')
plt.ylabel('Number of Orders')

plt.tight_layout()

plt.savefig(
    OUTPUT_PATH / '04_delivery_performance.png',
    dpi=300
)

plt.show()

# ============================================================
# EDA 5 — CUSTOMER SATISFACTION
# ============================================================

print('\n' + '=' * 60)
print('EDA 5 - CUSTOMER SATISFACTION')
print('=' * 60)

reviews = pd.read_csv(
    Path('data/processed') / 'order_reviews_cleaned.csv'
)

average_review_score = (
    reviews['review_score'].mean()
)

print(
    f'Average Review Score  :   '
    f'{average_review_score:.2f}'
)

review_distribution = (
    reviews['review_score']
    .value_counts()
    .sort_index()
)

print('\nReview Score Distribution:')
print(review_distribution)

plt.figure(figsize=(8,5))

sns.countplot(
    data=reviews,
    x='review_score',
    order=[1,2,3,4,5]
)

plt.title('Customer Review Score Distribution')
plt.xlabel('Review Score')
plt.ylabel('Number of Reviews')

plt.tight_layout()

plt.savefig(
    OUTPUT_PATH / '05_review_score_distribution.png',
    dpi=300
)

plt.show()

# ============================================================
# DELIVERY VS REVIEW SCORE
# ============================================================

delivery_review = (
    delivered_orders
    .groupby('delivery_performance')
    .agg(
        average_review_score=('review_score','mean')
    )
    .reset_index()
)

print('\nAverage Review Score by Delivery Performance:')

print(
    delivery_review
    .to_string(index=False)
)

# ============================================================
# SUMMARY
# ============================================================

print('\n' + '=' * 60)
print('EDA COMPLETED')
print('=' * 60)

print(
    f'EDA outputs saved to: {OUTPUT_PATH}'
)

