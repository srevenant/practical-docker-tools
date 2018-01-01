FROM python:3-alpine

WORKDIR /app
COPY requirements.txt docker-log-splitter startup.sh /app/

RUN pip3 install -r requirements.txt &&\
    rm -rf ~/.cache

ENTRYPOINT /app/startup.sh
