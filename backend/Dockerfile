FROM python:3.12-alpine

WORKDIR /app
COPY . ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 2 --threads 8  main:app 