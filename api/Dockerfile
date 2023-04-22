FROM python:latest

WORKDIR /opt/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:5001", "app:app"]