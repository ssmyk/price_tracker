FROM python:3.9
WORKDIR /scraper_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#ENV PYTHONPATH /scraper_app/tasks
#ENV FLASK_APP=app