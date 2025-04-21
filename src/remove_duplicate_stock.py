"""
Скрипт для удаления дублирующихся записей в таблице stock

Этот скрипт содержит SQL-запросы для идентификации и удаления дублирующихся записей
в таблице stock, где записи считаются дубликатами, если у них совпадают product_id и warehouse_id.

Подход к удалению дубликатов:
1. Создаем временную таблицу с уникальными записями, где для каждой комбинации product_id и warehouse_id
   сохраняется только одна запись с максимальным количеством товара
2. Удаляем все записи из основной таблицы
3. Вставляем данные из временной таблицы обратно в основную таблицу
"""

# Идентификация дубликатов
identification_query = """
SELECT product_id, warehouse_id, COUNT(*) as duplicate_count
FROM stock
GROUP BY product_id, warehouse_id
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;
"""

# Получение деталей о дубликатах (для проверки перед удалением)
details_query = """
SELECT s.stock_id, p.product_name, w.warehouse_name, s.quantity, s.last_restocked
FROM stock s
JOIN products p ON s.product_id = p.product_id
JOIN warehouses w ON s.warehouse_id = w.warehouse_id
WHERE (s.product_id, s.warehouse_id) IN (
    SELECT product_id, warehouse_id
    FROM stock
    GROUP BY product_id, warehouse_id
    HAVING COUNT(*) > 1
)
ORDER BY s.product_id, s.warehouse_id, s.stock_id;
"""

# Запрос для удаления дубликатов с сохранением одной записи с максимальным количеством
remove_duplicates_query = """
-- Создаем временную таблицу для хранения уникальных записей
CREATE TEMPORARY TABLE temp_stock AS
SELECT DISTINCT ON (product_id, warehouse_id) 
    stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at
FROM stock
ORDER BY product_id, warehouse_id, quantity DESC;

-- Удаляем все записи из основной таблицы
DELETE FROM stock;

-- Вставляем уникальные записи обратно в основную таблицу
INSERT INTO stock (stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at)
SELECT stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at
FROM temp_stock;

-- Удаляем временную таблицу
DROP TABLE temp_stock;
"""

# Запрос для объединения дубликатов (суммирование количества товаров)
merge_duplicates_query = """
-- Создаем временную таблицу для хранения объединенных записей
CREATE TEMPORARY TABLE temp_stock AS
SELECT 
    MIN(stock_id) as stock_id,
    product_id,
    warehouse_id,
    SUM(quantity) as quantity,
    MAX(last_restocked) as last_restocked,
    MIN(created_at) as created_at,
    MAX(updated_at) as updated_at
FROM stock
GROUP BY product_id, warehouse_id;

-- Удаляем все записи из основной таблицы
DELETE FROM stock;

-- Вставляем объединенные записи обратно в основную таблицу
INSERT INTO stock (stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at)
SELECT stock_id, product_id, warehouse_id, quantity, last_restocked, created_at, updated_at
FROM temp_stock;

-- Удаляем временную таблицу
DROP TABLE temp_stock;
"""

# Добавление уникального ограничения для предотвращения будущих дубликатов
add_unique_constraint_query = """
-- Добавляем уникальное ограничение на комбинацию product_id и warehouse_id
ALTER TABLE stock ADD CONSTRAINT unique_product_warehouse UNIQUE (product_id, warehouse_id);
"""

print("Скрипты для удаления дубликатов в таблице stock подготовлены.")
print("Для использования выполните один из запросов в вашей системе управления базами данных.")
print("Рекомендуется предварительно создать резервную копию базы данных!") 