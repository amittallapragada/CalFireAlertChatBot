FROM python:3.7-slim

USER root

WORKDIR /app

COPY app /app 

COPY ./requirements.txt /app/requirements.txt 
COPY ./background_jobs.sh /app/background_jobs.sh 

RUN chmod +x /app/background_jobs.sh 

RUN pip install -r requirements.txt 


CMD ["python", "update_jobs.py"]