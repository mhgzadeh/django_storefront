SELECT setval(pg_get_serial_sequence('store_order', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL)
FROM store_order;

select setval(pg_get_serial_sequence('store_orderitem', 'id'), coalesce(max(id), 1), max(id) is not null)
from store_orderitem;