FROM python:3.9

RUN apt-get update && apt-get -y install cron

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

COPY crontab /etc/cron.d/crontab

RUN touch /var/log/cron.log

RUN chmod 0644 /etc/cron.d/crontab

RUN crontab /etc/cron.d/crontab

CMD cron && tail -f /var/log/cron.log