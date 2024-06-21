export COMPOSE_FILE=docker-compose.yml

docker compose up -d --build broker statdb
sleep 10
docker compose run --build test

docker compose down
docker volume rm kafka_statdb
