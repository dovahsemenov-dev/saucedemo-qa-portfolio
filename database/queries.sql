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
