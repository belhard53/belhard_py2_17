FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt 

EXPOSE 5000

CMD ["python", "main1.py"]

