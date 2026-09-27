-- ============================================================
-- 01. CUSTOMER DISTRIBUTION BY STATE
-- ============================================================

SELECT
    customer_state,
    COUNT(*) AS total_customers
FROM olist_customers_dataset
GROUP BY customer_state
ORDER BY total_customers DESC
LIMIT 10;

-- ============================================================
-- 02. TOP 10 CUSTOMER CITIES
-- ============================================================

SELECT
    customer_city,
    COUNT(*) AS total_customers
FROM olist_customers_dataset
GROUP BY customer_city
ORDER BY total_customers DESC
LIMIT 10;

-- ============================================================
-- 03. ONE-TIME AND REPEAT CUSTOMERS ANALYSIS
-- ============================================================

-- OPTION 1: 3-Level Nested Subquery Approach
SELECT
	order_category,
    COUNT(*) AS jumlah
FROM (
	SELECT
	customer_unique_id,
	total_order,
	CASE
	WHEN total_order > 1 THEN 'Repeat'
	ELSE 'One-time'
    END AS order_category
	FROM (
		SELECT 
		c.customer_unique_id,
		COUNT(*) AS total_order
		FROM olist_customers_dataset AS c
		JOIN olist_orders_dataset AS o
		ON c.customer_id = o.customer_id
	WHERE o.order_status = 'delivered'
	GROUP BY c.customer_unique_id
	) AS floor_1
) AS floor_2
GROUP BY order_category;

-- OPTION 2: CTE (Common Table Expression) Refactored Approach (Recommended)
WITH floor_1 AS (
    SELECT 
        c.customer_unique_id,
        COUNT(*) AS total_order
    FROM olist_customers_dataset AS c
    JOIN olist_orders_dataset AS o
        ON c.customer_id = o.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
floor_2 AS (
    SELECT 
        customer_unique_id,
        total_order,
        CASE 
            WHEN total_order > 1 THEN 'Repeat'
            ELSE 'One-time'
        END AS order_category
    FROM floor_1
)
SELECT 
    order_category,
    COUNT(*) AS total_customers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM floor_2
GROUP BY order_category;

-- ============================================================
-- 04. MONTHLY REVENUE & ORDER VOLUME TREND ANALYSIS (DELIVERED ORDERS)
-- ============================================================

SELECT
	DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') as order_month,
    COUNT(DISTINCT o.order_id) as total_orders,
    ROUND(SUM(i.price), 2) as total_revenue
FROM olist_orders_dataset o
JOIN olist_order_items_dataset i
	ON o.order_id = i.order_id
WHERE o.order_status = 'delivered'
GROUP BY order_month
ORDER BY order_month;