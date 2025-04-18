-- Warehouse Management System Database Schema

-- Tables for warehouse management

-- Products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_description TEXT,
    category TEXT,
    unit_price NUMERIC NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT products_category_check CHECK (category = ANY (ARRAY['электроника'::TEXT, 'одежда'::TEXT, 'обувь'::TEXT, 'мебель'::TEXT, 'товары для спорта'::TEXT, 'инструменты'::TEXT, 'бытовая техника'::TEXT, 'здоровье'::TEXT, 'товары для дома'::TEXT, 'продукты'::TEXT])),
    CONSTRAINT products_unit_price_check CHECK (unit_price > 0)
);

-- Warehouses table
CREATE TABLE warehouses (
    warehouse_id SERIAL PRIMARY KEY,
    warehouse_name TEXT NOT NULL,
    location TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT warehouses_capacity_check CHECK (capacity > 0)
);

-- Stock table
CREATE TABLE stock (
    stock_id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(product_id) ON DELETE CASCADE,
    warehouse_id INTEGER REFERENCES warehouses(warehouse_id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    last_restocked DATE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT stock_quantity_check CHECK (quantity >= 0)
);

-- Create indexes for stock table
CREATE INDEX idx_stock_product_id ON stock(product_id);
CREATE INDEX idx_stock_warehouse_id ON stock(warehouse_id);

-- Suppliers table
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name TEXT NOT NULL,
    contact_person TEXT,
    phone_number TEXT,
    email TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT suppliers_email_check CHECK (email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
    CONSTRAINT suppliers_phone_number_check CHECK (phone_number ~ '^\d{11}$'),
    CONSTRAINT suppliers_phone_number_not_null CHECK (phone_number IS NOT NULL)
);

-- Orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    supplier_id INTEGER REFERENCES suppliers(supplier_id) ON DELETE CASCADE,
    total_amount NUMERIC NOT NULL,
    status TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT orders_status_check CHECK (status = ANY (ARRAY['в обработке'::TEXT, 'доставлен'::TEXT, 'отменен'::TEXT])),
    CONSTRAINT orders_total_amount_check CHECK (total_amount > 0)
);

-- Order items table
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(product_id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC NOT NULL,
    total_price NUMERIC NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT order_items_quantity_check CHECK (quantity > 0),
    CONSTRAINT order_items_unit_price_check CHECK (unit_price > 0),
    CONSTRAINT order_items_total_price_check CHECK (total_price > 0)
);

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Functions and triggers

-- Function to update stock when new order items are added
CREATE OR REPLACE FUNCTION update_stock_quantity()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE stock 
    SET quantity = quantity + NEW.quantity,
        last_restocked = CURRENT_DATE,
        updated_at = CURRENT_TIMESTAMP
    WHERE product_id = NEW.product_id AND 
          warehouse_id = (SELECT warehouse_id FROM stock WHERE product_id = NEW.product_id LIMIT 1);
    
    -- If the product doesn't exist in any warehouse yet, add it to the first warehouse
    IF NOT FOUND THEN
        INSERT INTO stock (product_id, warehouse_id, quantity, last_restocked)
        VALUES (NEW.product_id, 
                (SELECT warehouse_id FROM warehouses ORDER BY warehouse_id LIMIT 1), 
                NEW.quantity, 
                CURRENT_DATE);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update stock on order delivery
CREATE TRIGGER after_order_delivered
AFTER UPDATE ON orders
FOR EACH ROW
WHEN (NEW.status = 'доставлен' AND OLD.status = 'в обработке')
EXECUTE FUNCTION update_stock_quantity();

-- Function to calculate total price for order items
CREATE OR REPLACE FUNCTION calculate_order_item_total()
RETURNS TRIGGER AS $$
BEGIN
    NEW.total_price = NEW.unit_price * NEW.quantity;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to calculate total price before inserting order item
CREATE TRIGGER before_order_item_insert
BEFORE INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION calculate_order_item_total();

-- Часть 21: Правила (Rules) в PostgreSQL
-- 1.	Создание правила (Rule) для автоматического обновления:
-- Создайте правило, которое автоматически обновляет поле updated_at в таблице products каждый раз, когда товар изменяется.

CREATE OR REPLACE FUNCTION public.update_products_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP; -- Устанавливаем текущее время
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER products_update_trigger
BEFORE UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION update_products_updated_at();

-- 2.	Использование правил для автоматических операций:
-- Напишите правило, которое будет автоматически удалять запись из таблицы stock, если количество товара на складе меньше 0.
CREATE OR REPLACE RULE delete_negative_stock AS
ON UPDATE TO public.stock
WHERE NEW.quantity <= 0
DO INSTEAD DELETE FROM public.stock WHERE stock_id = NEW.stock_id;

-- Initial data

-- Add default admin and manager users
INSERT INTO users (username, password_hash, full_name, is_admin, email) VALUES
('admin', 'admin123', 'Администратор Системы', TRUE, 'admin@warehouse.ru'),
('manager', 'manager123', 'Менеджер Склада', FALSE, 'manager@warehouse.ru');

-- Add example warehouses
INSERT INTO warehouses (warehouse_name, location, capacity) VALUES
('Основной склад', 'Москва, ул. Складская, 1', 10000),
('Северный склад', 'Санкт-Петербург, пр. Логистический, 5', 8000),
('Южный склад', 'Краснодар, ул. Транспортная, 15', 5000);

-- Add example suppliers
INSERT INTO suppliers (supplier_name, contact_person, phone_number, email) VALUES
('ООО Техноснаб', 'Иванов Иван', '79001234567', 'ivanov@technosnab.ru'),
('АО ЭлектроТрейд', 'Петров Петр', '79991234567', 'petrov@electrotrade.ru'),
('ИП Сидоров', 'Сидоров Алексей', '79161234567', 'sidorov@mail.ru');

-- Add example products
INSERT INTO products (product_name, product_description, category, unit_price) VALUES
('Смартфон Galaxy S21', 'Мощный смартфон с отличной камерой', 'электроника', 79999.99),
('Ноутбук Pro 15', '15-дюймовый ноутбук для работы', 'электроника', 115000.00),
('Кроссовки Runner', 'Спортивные кроссовки для бега', 'обувь', 5999.50),
('Диван Modern', 'Трехместный диван в современном стиле', 'мебель', 45000.00),
('Телевизор 55" Smart TV', '4K Smart TV с HDR', 'бытовая техника', 49999.00),
('Фитнес-браслет Track 3', 'Трекер активности с мониторингом сна', 'товары для спорта', 3499.00),
('Утюг Smooth', 'Паровой утюг с антипригарным покрытием', 'бытовая техника', 2999.00),
('Набор инструментов Profi', 'Профессиональный набор из 150 инструментов', 'инструменты', 8999.00),
('Шампунь Herbal', 'Шампунь с натуральными экстрактами', 'здоровье', 349.90),
('Полотенце Deluxe', 'Мягкое хлопковое полотенце', 'товары для дома', 799.50);

-- Add initial stock
INSERT INTO stock (product_id, warehouse_id, quantity, last_restocked) VALUES
(1, 1, 50, CURRENT_DATE),
(2, 1, 30, CURRENT_DATE),
(3, 1, 100, CURRENT_DATE),
(4, 1, 15, CURRENT_DATE),
(5, 1, 25, CURRENT_DATE),
(6, 2, 80, CURRENT_DATE),
(7, 2, 60, CURRENT_DATE),
(8, 2, 40, CURRENT_DATE),
(9, 3, 200, CURRENT_DATE),
(10, 3, 150, CURRENT_DATE);

-- Add example orders
INSERT INTO orders (order_date, supplier_id, total_amount, status) VALUES
(CURRENT_DATE - INTERVAL '10 days', 1, 240000.00, 'доставлен'),
(CURRENT_DATE - INTERVAL '5 days', 2, 150000.00, 'доставлен'),
(CURRENT_DATE - INTERVAL '2 days', 3, 80000.00, 'в обработке'),
(CURRENT_DATE, 1, 35000.00, 'в обработке');

-- Add example order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(1, 1, 20, 75000.00, 1500000.00),
(1, 5, 15, 48000.00, 720000.00),
(2, 3, 50, 5800.00, 290000.00),
(2, 6, 100, 3300.00, 330000.00),
(3, 8, 30, 8500.00, 255000.00),
(3, 10, 100, 750.00, 75000.00),
(4, 4, 5, 43000.00, 215000.00),
(4, 7, 40, 2800.00, 112000.00); 