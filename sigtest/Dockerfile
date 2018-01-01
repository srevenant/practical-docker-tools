FROM python:3-alpine
WORKDIR /app/
COPY sigtest.py startup.sh forked.sh /app/
ENTRYPOINT ["./startup.sh"]
#ENTRYPOINT ["python3", "sigtest.py"]
