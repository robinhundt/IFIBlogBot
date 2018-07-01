FROM python:3.6-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir /db
VOLUME /db

ENV PYTHONPATH .
CMD [ "python", "./src/ifi_bot.py" ]

