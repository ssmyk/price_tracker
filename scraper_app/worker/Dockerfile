FROM python:3.9
WORKDIR /worker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH "${PYTHONPATH}:/worker/"
ENTRYPOINT celery -A scraper worker --loglevel=INFO

#ENV FLASK_APP=scraper_api

