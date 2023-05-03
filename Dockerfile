FROM python:3.9

WORKDIR /app

COPY . .
RUN pip install  -r requirements.txt

RUN crontab crontab
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log