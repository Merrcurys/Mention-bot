FROM python:3.15.0-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN touch /app/logs.log

CMD ["python", "bot.py"]