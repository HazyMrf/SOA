FROM python:3.9

WORKDIR /
COPY ./post_service/* .
COPY ./post_service.proto .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. post_service.proto

CMD [ "python", "./post_service.py" ]
