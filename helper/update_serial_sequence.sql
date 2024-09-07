SELECT setval(pg_get_serial_sequence('store_product', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL)
FROM store_product;