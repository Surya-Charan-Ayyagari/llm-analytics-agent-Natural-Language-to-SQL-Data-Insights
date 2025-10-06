-- Simple sales schema for demos
CREATE TABLE IF NOT EXISTS dim_product (
product_id SERIAL PRIMARY KEY,
product_name TEXT NOT NULL,
category TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS fact_sales (
sale_id SERIAL PRIMARY KEY,
order_date DATE NOT NULL,
region TEXT NOT NULL,
product_id INT NOT NULL REFERENCES dim_product(product_id),
units INT NOT NULL,
unit_price NUMERIC(10,2) NOT NULL,
discount NUMERIC(5,2) DEFAULT 0.0
);


-- Seed data
INSERT INTO dim_product (product_name, category) VALUES
('Alpha Widget','Gadgets'),('Beta Widget','Gadgets'),('Gamma Gizmo','Gizmos')
ON CONFLICT DO NOTHING;


INSERT INTO fact_sales (order_date,region,product_id,units,unit_price,discount) VALUES
('2024-01-15','Midwest',1,120,19.99,0.05),
('2024-02-20','West',2,80,24.50,0.10),
('2024-03-11','South',3,60,39.00,0.00),
('2024-04-07','Midwest',2,130,24.50,0.00),
('2024-05-22','East',1,95,19.99,0.15),
('2024-06-18','West',3,77,39.00,0.05),
('2024-07-07','South',1,88,19.99,0.00),
('2024-08-19','East',2,110,24.50,0.05),
('2024-09-05','West',1,150,19.99,0.10)
ON CONFLICT DO NOTHING;


-- Helpful computed view
CREATE OR REPLACE VIEW v_sales_detailed AS
SELECT
s.sale_id,
s.order_date,
date_trunc('month', s.order_date)::date AS order_month,
s.region,
p.product_name,
p.category,
s.units,
s.unit_price,
s.discount,
(s.units * s.unit_price * (1 - s.discount))::numeric(12,2) AS revenue
FROM fact_sales s
JOIN dim_product p ON p.product_id = s.product_id;
