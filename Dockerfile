FROM python:3.13.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN touch /app/logs.log

EXPOSE 8001

CMD ["python", "bot.py"]