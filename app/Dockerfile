FROM python:3.9

WORKDIR /
COPY ./app/* .
COPY ./post_service.proto .
COPY ./stat_service.proto .

RUN chmod +x entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. post_service.proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. stat_service.proto

ENV FLASK_APP=app.py
ENTRYPOINT ["./entrypoint.sh"]
