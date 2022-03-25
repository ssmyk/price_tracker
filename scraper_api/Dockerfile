FROM python:3.9
WORKDIR /scraper_api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#ENV PYTHONPATH "${PYTHONPATH}:/worker/"
#ENV FLASK_APP=scraper_api

