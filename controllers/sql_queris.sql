-- Query name: product_sales_summary
SELECT product_name, SUM(amount) AS total_sales
FROM invoices
GROUP BY product_name;

-- Query name: event_sales_summary
SELECT event_id, SUM(amount) AS total_sales
FROM invoices
GROUP BY event_id;

-- Query name: avg_purchase_by_ui_and_desc
SELECT ui_change, desc_change, AVG(amount) AS avg_purchase
FROM test_analysis
JOIN invoices ON test_analysis.userid = invoices.userid
GROUP BY ui_change, desc_change;

-- Query name: avg_purchase_by_product_ui_desc
SELECT product_name, ui_change, desc_change, AVG(amount) AS avg_purchase
FROM test_analysis
JOIN invoices ON test_analysis.userid = invoices.userid
JOIN products ON invoices.event_id = products.event_id
GROUP BY product_name, ui_change, desc_change;

-- Query name: product_sales_statistics
SELECT 
    product_name,
    AVG(amount) AS avg_sales,
    SQRT(SUM((amount - avg_amount) * (amount - avg_amount)) / COUNT(amount)) AS std_sales,
    MIN(amount) AS min_sales,
    MAX(amount) AS max_sales
FROM (
    SELECT 
        product_name, 
        amount,
        AVG(amount) OVER (PARTITION BY product_name) AS avg_amount
    FROM invoices
) AS subquery
GROUP BY product_name;


-- Query name: ui_description_sales_summary
SELECT 
    ui_change, 
    desc_change, 
    SUM(amount) AS total_sales
FROM test_analysis
JOIN invoices ON test_analysis.userid = invoices.userid
GROUP BY ui_change, desc_change;

-- Query name: final_data_query
SELECT 
    p.event_name, 
    i.amount, 
    t.ui_change, 
    t.desc_change
FROM invoices i
JOIN products p ON i.event_id = p.event_id  -- Join with the tbl_products to get event_name
JOIN test_analysis t ON i.userid = t.userid


-- Query name: product_sales_by_group
SELECT 
    CASE 
        WHEN COALESCE(ui_change, 'no') = 'no' AND COALESCE(desc_change, 'no') = 'no' THEN 'A'
        WHEN COALESCE(ui_change, 'no') = 'yes' AND COALESCE(desc_change, 'no') = 'no' THEN 'B'
        WHEN COALESCE(ui_change, 'no') = 'no' AND COALESCE(desc_change, 'yes') = 'yes' THEN 'C'
        WHEN COALESCE(ui_change, 'no') = 'yes' AND COALESCE(desc_change, 'yes') = 'yes' THEN 'D'
        ELSE 'Unknown'  -- In case there's an unexpected combination
    END AS group_name,
    SUM(i.amount) AS total_sales
FROM test_analysis t
JOIN invoices i ON t.userid = i.userid
GROUP BY group_name;

-- Query name: monthly_sales_query
SELECT amount, datepaid
FROM invoices;

-- Query name: z_score
SELECT amount FROM invoices WHERE amount IS NOT NULL