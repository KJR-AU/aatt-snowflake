-- Create a dedicated schema
CREATE DATABASE IF NOT EXISTS dlt_demo
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
USE dlt_demo;

-- Customers
CREATE TABLE customers (
  customer_id      BIGINT PRIMARY KEY AUTO_INCREMENT,
  external_id      VARCHAR(64) UNIQUE,
  first_name       VARCHAR(100),
  last_name        VARCHAR(100),
  email            VARCHAR(255) UNIQUE,
  phone            VARCHAR(32),
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Addresses (supports multiple per customer)
CREATE TABLE addresses (
  address_id       BIGINT PRIMARY KEY AUTO_INCREMENT,
  customer_id      BIGINT NOT NULL,
  address_type     ENUM('billing','shipping') NOT NULL,
  line1            VARCHAR(255) NOT NULL,
  line2            VARCHAR(255),
  city             VARCHAR(120) NOT NULL,
  state            VARCHAR(120),
  postal_code      VARCHAR(32),
  country          CHAR(2) NOT NULL,
  is_primary       TINYINT(1) NOT NULL DEFAULT 0,
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_addr_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
) ENGINE=InnoDB;

-- Products
CREATE TABLE products (
  product_id       BIGINT PRIMARY KEY AUTO_INCREMENT,
  sku              VARCHAR(64) NOT NULL UNIQUE,
  name             VARCHAR(255) NOT NULL,
  category         VARCHAR(120),
  unit_price       DECIMAL(10,2) NOT NULL,
  currency         CHAR(3) NOT NULL DEFAULT 'USD',
  active           TINYINT(1) NOT NULL DEFAULT 1,
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Orders
CREATE TABLE orders (
  order_id             BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_number         VARCHAR(64) NOT NULL UNIQUE,
  customer_id          BIGINT NOT NULL,
  order_date           DATETIME NOT NULL,
  status               ENUM('pending','paid','shipped','cancelled','refunded') NOT NULL DEFAULT 'pending',
  total_amount         DECIMAL(12,2) NOT NULL,
  currency             CHAR(3) NOT NULL DEFAULT 'USD',
  billing_address_id   BIGINT,
  shipping_address_id  BIGINT,
  created_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_orders_customer  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  CONSTRAINT fk_orders_bill_addr FOREIGN KEY (billing_address_id) REFERENCES addresses(address_id),
  CONSTRAINT fk_orders_ship_addr FOREIGN KEY (shipping_address_id) REFERENCES addresses(address_id),
  INDEX idx_orders_customer_date (customer_id, order_date)
) ENGINE=InnoDB;

-- Order items
CREATE TABLE order_items (
  order_item_id    BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_id         BIGINT NOT NULL,
  product_id       BIGINT NOT NULL,
  quantity         INT NOT NULL CHECK (quantity > 0),
  unit_price       DECIMAL(10,2) NOT NULL,
  line_amount      DECIMAL(12,2) AS (quantity * unit_price) STORED,
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_items_order   FOREIGN KEY (order_id) REFERENCES orders(order_id),
  CONSTRAINT fk_items_product FOREIGN KEY (product_id) REFERENCES products(product_id),
  INDEX idx_items_order (order_id)
) ENGINE=InnoDB;

-- Payments
CREATE TABLE payments (
  payment_id       BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_id         BIGINT NOT NULL,
  method           ENUM('card','paypal','bank_transfer','gift_card') NOT NULL,
  amount           DECIMAL(12,2) NOT NULL,
  currency         CHAR(3) NOT NULL DEFAULT 'USD',
  status           ENUM('authorized','captured','failed','refunded') NOT NULL,
  transaction_ref  VARCHAR(128),
  paid_at          DATETIME,
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_payments_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
  INDEX idx_payments_order (order_id)
) ENGINE=InnoDB;

-- Semi-structured events for Snowflake VARIANT testing
CREATE TABLE events (
  event_id     BIGINT PRIMARY KEY AUTO_INCREMENT,
  event_type   VARCHAR(64) NOT NULL,
  customer_id  BIGINT,
  order_id     BIGINT,
  payload      JSON NOT NULL,
  created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_events_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  CONSTRAINT fk_events_order    FOREIGN KEY (order_id)    REFERENCES orders(order_id),
  INDEX idx_events_type_time (event_type, created_at)
) ENGINE=InnoDB;

-- Seed data -------------------------------------------------------------

-- Customers
INSERT INTO customers (external_id, first_name, last_name, email, phone, created_at)
VALUES
('CUST-001','Ava','Nguyen','ava.nguyen@example.com','+61 400 111 111','2025-08-20 09:15:00'),
('CUST-002','Liam','Smith','liam.smith@example.com','+61 400 222 222','2025-08-22 14:05:00'),
('CUST-003','Noah','Chen','noah.chen@example.com','+61 400 333 333','2025-08-25 11:30:00'),
('CUST-004','Mia','Patel','mia.patel@example.com','+61 400 444 444','2025-08-26 16:45:00'),
('CUST-005','Zoe','Johnson','zoe.johnson@example.com','+61 400 555 555','2025-08-27 10:10:00');

-- Addresses
INSERT INTO addresses (customer_id, address_type, line1, line2, city, state, postal_code, country, is_primary)
VALUES
(1,'billing','10 River St',NULL,'Brisbane','QLD','4000','AU',1),
(1,'shipping','10 River St',NULL,'Brisbane','QLD','4000','AU',1),
(2,'billing','55 Market Rd','Unit 9','Sydney','NSW','2000','AU',1),
(2,'shipping','88 Harbour Dr',NULL,'Sydney','NSW','2000','AU',1),
(3,'billing','12 Green Ave',NULL,'Melbourne','VIC','3000','AU',1),
(4,'billing','7 Coral Pl',NULL,'Perth','WA','6000','AU',1),
(5,'billing','2 Wattle St',NULL,'Adelaide','SA','5000','AU',1);

-- Products
INSERT INTO products (sku, name, category, unit_price, currency, active, created_at)
VALUES
('SKU-100','Wireless Mouse','Accessories',29.99,'AUD',1,'2025-08-15 08:00:00'),
('SKU-101','Mechanical Keyboard','Accessories',129.00,'AUD',1,'2025-08-15 08:05:00'),
('SKU-102','27in Monitor','Displays',349.00,'AUD',1,'2025-08-15 08:10:00'),
('SKU-103','USB-C Hub','Accessories',59.50,'AUD',1,'2025-08-15 08:15:00'),
('SKU-104','Laptop Stand','Accessories',44.00,'AUD',1,'2025-08-15 08:20:00');

-- Orders
INSERT INTO orders (order_number, customer_id, order_date, status, total_amount, currency, billing_address_id, shipping_address_id, created_at)
VALUES
('ORD-0001',1,'2025-08-28 09:00:00','paid',158.99,'AUD',1,2,'2025-08-28 09:00:00'),
('ORD-0002',2,'2025-08-29 10:30:00','paid',349.00,'AUD',3,4,'2025-08-29 10:30:00'),
('ORD-0003',2,'2025-08-30 13:20:00','shipped',188.50,'AUD',3,4,'2025-08-30 13:20:00'),
('ORD-0004',3,'2025-09-01 15:45:00','cancelled',59.50,'AUD',5,NULL,'2025-09-01 15:45:00'),
('ORD-0005',4,'2025-09-02 11:10:00','pending',473.99,'AUD',6,NULL,'2025-09-02 11:10:00'),
('ORD-0006',5,'2025-09-03 16:25:00','refunded',129.00,'AUD',7,NULL,'2025-09-03 16:25:00');

-- Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, created_at)
VALUES
(1,1,1,29.99,'2025-08-28 09:00:00'),
(1,3,1,349.00,'2025-08-28 09:00:00'), -- note: total on order intentionally smaller than sum to simulate discounts/rounding in downstream transforms
(2,3,1,349.00,'2025-08-29 10:30:00'),
(3,4,2,59.50,'2025-08-30 13:20:00'),
(3,5,1,44.00,'2025-08-30 13:20:00'),
(4,4,1,59.50,'2025-09-01 15:45:00'),
(5,2,1,129.00,'2025-09-02 11:10:00'),
(5,1,2,29.99,'2025-09-02 11:10:00'),
(5,5,1,44.00,'2025-09-02 11:10:00'),
(6,2,1,129.00,'2025-09-03 16:25:00');

-- Payments
INSERT INTO payments (order_id, method, amount, currency, status, transaction_ref, paid_at, created_at)
VALUES
(1,'card',158.99,'AUD','captured','TXN-A1001','2025-08-28 09:05:00','2025-08-28 09:05:00'),
(2,'paypal',349.00,'AUD','captured','TXN-A1002','2025-08-29 10:35:00','2025-08-29 10:35:00'),
(3,'card',188.50,'AUD','captured','TXN-A1003','2025-08-30 13:25:00','2025-08-30 13:25:00'),
(4,'card',59.50,'AUD','failed','TXN-A1004',NULL,'2025-09-01 15:50:00'),
(5,'bank_transfer',473.99,'AUD','authorized','TXN-A1005','2025-09-02 12:00:00','2025-09-02 12:00:00'),
(6,'card',129.00,'AUD','refunded','TXN-A1006','2025-09-03 16:30:00','2025-09-03 16:30:00');

-- Events (JSON payloads for Snowflake VARIANT)
INSERT INTO events (event_type, customer_id, order_id, payload, created_at)
VALUES
('page_view', 1, NULL, JSON_OBJECT('path','/home','referrer',NULL,'device',JSON_OBJECT('type','mobile','os','iOS')), '2025-08-28 08:59:10'),
('add_to_cart', 1, NULL, JSON_OBJECT('sku','SKU-100','qty',1,'price',29.99), '2025-08-28 08:59:40'),
('checkout_started', 1, 1, JSON_OBJECT('order_number','ORD-0001','items',JSON_ARRAY(JSON_OBJECT('sku','SKU-100','qty',1))), '2025-08-28 09:00:10'),
('payment_attempt', 1, 1, JSON_OBJECT('method','card','status','success','auth_code','A1B2C3'), '2025-08-28 09:05:05'),
('shipment_update', 2, 3, JSON_OBJECT('carrier','AUSPOST','status','in_transit','eta','2025-09-03'), '2025-08-31 09:10:00'),
('refund_issued', 5, 6, JSON_OBJECT('amount',129.00,'reason','defective','initiated_by','customer'), '2025-09-04 10:00:00');

-- Useful indexes (optional but helpful for DLT joins & CDC-like tests)
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_products_sku ON products(sku);
