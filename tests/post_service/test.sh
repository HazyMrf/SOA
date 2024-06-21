export COMPOSE_FILE=docker-compose.yml

docker compose up -d --build post_service postdb
sleep 10
python3 -m unittest service_test.py 

docker compose down
docker volume rm post_service_postdb_postgres_data