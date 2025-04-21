-- Исправленная функция для обновления остатков на складе
CREATE OR REPLACE FUNCTION update_stock_quantity()
RETURNS TRIGGER AS $$
DECLARE
    item RECORD;
BEGIN
    -- Проходим по всем позициям заказа и обновляем запасы на складе
    FOR item IN (SELECT product_id, quantity FROM order_items WHERE order_id = NEW.order_id)
    LOOP
        -- Обновляем существующие записи в stock
        UPDATE stock 
        SET quantity = quantity + item.quantity,
            last_restocked = CURRENT_DATE,
            updated_at = CURRENT_TIMESTAMP
        WHERE product_id = item.product_id AND 
              warehouse_id = (SELECT warehouse_id FROM stock WHERE product_id = item.product_id LIMIT 1);
        
        -- Если товар не найден ни на одном складе, добавляем его на первый склад
        IF NOT FOUND THEN
            INSERT INTO stock (product_id, warehouse_id, quantity, last_restocked)
            VALUES (item.product_id, 
                    (SELECT warehouse_id FROM warehouses ORDER BY warehouse_id LIMIT 1), 
                    item.quantity, 
                    CURRENT_DATE);
        END IF;
    END LOOP;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для вызова функции после изменения статуса заказа на 'доставлен'
DROP TRIGGER IF EXISTS after_order_delivered ON orders;

CREATE TRIGGER after_order_delivered
AFTER UPDATE ON orders
FOR EACH ROW
WHEN (NEW.status = 'доставлен' AND OLD.status = 'в обработке')
EXECUTE FUNCTION update_stock_quantity(); 