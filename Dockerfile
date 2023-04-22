FROM python:latest

WORKDIR /opt/discord_bot

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
