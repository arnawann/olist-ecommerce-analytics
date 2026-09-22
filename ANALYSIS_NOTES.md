# Analysis Notes
Dan saya akan ingatkan setiap kali:

> 📝 **Ini masuk Analysis Notes + report**  
> 🟡 **Ini masuk Analysis Notes sebagai supporting**  
> ❌ **Ini tidak perlu dicatat sebagai finding**

Jadi project-mu nantinya bukan cuma kumpulan kode, tetapi punya **jejak cara berpikir seorang Data Analyst**.

## 01. Customer Distribution by State

### Business Question
Where are Olist customers geographically concentrated?

### SQL
```sql
SELECT
    customer_state,
    COUNT(*) AS total_customers
FROM olist_customers_dataset
GROUP BY customer_state
ORDER BY total_customers DESC;

Result
SP: 41,746
RJ: 12,852
MG: 11,635

Insight
Customers are highly concentrated in São Paulo (SP), followed by Rio de Janeiro (RJ) and Minas Gerais (MG).

Report Status
📝 CATAT

## 02. Top 10 Customer Cities
### SQL
SELECT
    customer_city,
    COUNT(*) AS total_customers
FROM olist_customers_dataset
GROUP BY customer_city
ORDER BY total_customers DESC
LIMIT 10;

Result
São Paulo	15,540
Rio de Janeiro	6,882
Belo Horizonte	2,773

Insight
Customer records are concentrated in a small number of major cities, with São Paulo having the largest number.

Report Status
📝 CATAT

## 03. Repeat vs One-time customers

### Business Question
Of all Olist customers, how many have shopped only once, and how many have made more than one purchase?

### SQL
SELECT
    c.customer_unique_id,o.order_id, 
    customer_id, 
    COUNT(*)
FROM olist_customers_dataset AS c, olist_orders_dataset AS o
JOIN o.order_id ON c.customer_id = o.customer_id
GROUP BY customer_unique_id;

Your results:

One-time customers: 90,557
Repeat customers: 2,801

So, the total number of customers who have had at least one order delivered:

90,557 + 2,801 = 93,358 customers

If we look at the proportions:

One-time: ≈ 97.0%
Repeat: ≈ 3.0%

Of the 93,358 customers who had at least one delivered order, 90,557 customers (≈97%) made only one purchase, while 2,801 customers (≈3%) made more than one purchase.