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
    STDDEV(amount) AS std_sales,
    MIN(amount) AS min_sales,
    MAX(amount) AS max_sales
FROM invoices
GROUP BY product_name;

-- Query name: ui_description_sales_summary
SELECT 
    ui_change, 
    desc_change, 
    SUM(amount) AS total_sales
FROM test_analysis
JOIN invoices ON test_analysis.userid = invoices.userid
GROUP BY ui_change, desc_change;

