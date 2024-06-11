# Парфененко Илья Олегович

## Сборка приложения
* docker compose build
* docker compose up -d post_service
* docker compose up app
Не забывайте чистить volume баз данных через `docker volume rm $(docker volume ls -q)`.

## cURL запросы для проверки валидности приложения

### Регистрация/персоналка пользователя:

* Регистрация пользователя:

    * `curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username":"newuser", "password":"newpassword"}'`

* Вход пользователя:

    * `curl -c cookie.txt -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username":"newuser", "password":"newpassword"}'`

* Обновление персональных данных:

    * `curl -b cookie.txt -X PUT http://localhost:5000/update_profile  -H "Content-Type: application/json" -d '{"first_name": "Иван", "last_name": "Иванов"}'`

### `gRPC` запросы:

* Создание поста:

    * `curl -b cookie.txt -X POST http://localhost:5000/posts  -H "Content-Type: application/json" -d '{"title": "POOOOOST", "content": "ZIP NAN EMPTY"}'`

* Обновление поста:

    * `curl -b cookie.txt -X PUT http://localhost:5000/posts/POST_ID  -H "Content-Type: application/json" -d '{"title": "POOOOOST", "content": "ZEBRA"}'`

* Удаление поста:

    * `curl -b cookie.txt -X DELETE http://localhost:5000/posts/POST_ID  -H "Content-Type: application/json"`

* Получение конкретного поста:

    * `curl -b cookie.txt -X GET http://localhost:5000/posts/POST_ID  -H "Content-Type: application/json"`

* Получение постов с пагинацией

    * `curl -b cookie.txt -X GET http://localhost:5000/posts -H "Content-Type: application/json" -d '{"page_number": "1", "posts_per_page": "10"}'`

