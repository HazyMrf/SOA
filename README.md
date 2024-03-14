Парфененко Илья Олегович

Для того, чтобы поднять приложение (любой из 2ух вариантов)
* docker compose build && docker compose up
* docker compose up -d --build (detached режим)

Возможные cURL запросы для проверки валидности приложения:

Регистрация пользователя:
`curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username":"newuser", "password":"newpassword"}'`

Вход пользователя:
`curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username":"newuser", "password":"newpassword"}'`

Обновление персональных данных:


Не забывайте чистить volume базы данных через `docker volume rm`.
