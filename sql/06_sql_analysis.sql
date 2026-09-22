-- ============================================================
-- 01. CUSTOMER DISTRIBUTION BY STATE
-- ============================================================

SELECT
    customer_state,
    COUNT(*) AS total_customers
FROM olist_customers_dataset
GROUP BY customer_state
ORDER BY total_customers DESC;
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