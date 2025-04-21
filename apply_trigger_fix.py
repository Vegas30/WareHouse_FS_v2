import psycopg2
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname="test_db",
        user="postgres",
        password="7773", 
        host="localhost",
        port="5432"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    logger.info("Подключение к базе данных успешно")
    
    # Создаем SQL-скрипт непосредственно в коде
    sql_script = """
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
    """
    
    # Выполнение SQL-скрипта
    cursor.execute(sql_script)
    logger.info("Триггер успешно обновлен")
    
    # Проверка результата
    cursor.execute("""
        SELECT routine_name 
        FROM information_schema.routines 
        WHERE routine_name = 'update_stock_quantity'
    """)
    result = cursor.fetchone()
    if result:
        logger.info(f"Функция {result[0]} существует в базе данных")
    
    cursor.execute("""
        SELECT trigger_name 
        FROM information_schema.triggers 
        WHERE event_object_table = 'orders' AND trigger_name = 'after_order_delivered'
    """)
    result = cursor.fetchone()
    if result:
        logger.info(f"Триггер {result[0]} существует в базе данных")
    else:
        logger.warning("Триггер не найден в information_schema.triggers")
        
        # Альтернативный способ проверки наличия триггера
        cursor.execute("""
            SELECT tgname FROM pg_trigger 
            JOIN pg_class ON pg_trigger.tgrelid = pg_class.oid
            WHERE relname = 'orders' AND tgname = 'after_order_delivered'
        """)
        result = cursor.fetchone()
        if result:
            logger.info(f"Триггер {result[0]} существует в pg_trigger")
    
    # Закрытие подключения
    cursor.close()
    conn.close()
    logger.info("Соединение с базой данных закрыто")
    
    print("Триггер для обновления остатков на складе успешно обновлен!")
    
except Exception as e:
    logger.error(f"Ошибка: {str(e)}")
    print(f"Произошла ошибка: {str(e)}") 