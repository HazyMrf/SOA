FROM python:3.9
WORKDIR /
COPY . .
RUN chmod +x entrypoint.sh

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENTRYPOINT ["./entrypoint.sh"]