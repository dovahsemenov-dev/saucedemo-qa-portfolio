Скрипты и SQL-запросы для базы данных интернет-магазина Swag Labs

 1.Выбор всех активных пользователей из таблицы для проверки доступов
SELECT * FROM users WHERE status = 'active';

2.Поиск конкретного пользователя по его логину для проверки авторизации
SELECT id, username, role FROM users WHERE username = 'standard_user';

3.Вывод списка товаров, отсортированных по цене от самых дорогих к дешевым (проверка логики сортировки каталога)
SELECT product_name, price FROM products ORDER BY price DESC;

4.Подсчет общего количества товаров в категории "одежда"
SELECT COUNT(*) FROM products WHERE category = 'clothing';

5.Запрос для проверки корзины: смотрим, какие товары добавил конкретный пользователь (объединение таблиц через JOIN)
SELECT users.username, cart.product_id, cart.quantity 
FROM cart 
JOIN users ON cart.user_id = users.id 
WHERE users.username = 'standard_user';

6.Количество товаров в каждой категории: GROUP BY по полю категории
SELECT category, COUNT(*) AS products_count
FROM products
GROUP BY category;

7.Категории с числом товаров больше одного: HAVING после GROUP BY
SELECT category, COUNT(*) AS products_count
FROM products
GROUP BY category
HAVING COUNT(*) > 1;

8.Пользователи, у которых уже есть товары в корзине: подзапрос в WHERE
SELECT username
FROM users
WHERE id IN (SELECT DISTINCT user_id FROM cart);

9.Заказы с суммой выше средней: подзапрос как выражение в сравнении
SELECT order_id, total_amount
FROM orders
WHERE total_amount > (SELECT AVG(total_amount) FROM orders);

10.Товары из корзины standard_user с их ценой и суммой позиции: JOIN + вычисляемое поле
SELECT p.product_name,
       p.price,
       c.quantity,
       p.price * c.quantity AS position_total
FROM cart c
JOIN products p ON p.id = c.product_id
JOIN users u ON u.id = c.user_id
WHERE u.username = 'standard_user'
ORDER BY position_total DESC;
