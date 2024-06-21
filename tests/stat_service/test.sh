export COMPOSE_FILE=docker-compose.yml

docker compose up -d --build statdb stat_service
sleep 10
python3 -m unittest service_test.py 

docker compose down
docker volume rm stat_service_statdb