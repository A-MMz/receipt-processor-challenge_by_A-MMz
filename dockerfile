FROM python:3.11.6-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir Flask

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production


CMD ["flask", "run"]
