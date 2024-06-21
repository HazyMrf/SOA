FROM python:3.9

WORKDIR /
COPY ./stat_service/* .
COPY ./stat_service.proto .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. stat_service.proto

CMD [ "python", "./stat_service.py" ]
