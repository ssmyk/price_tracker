FROM python:3.9
WORKDIR /web_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#RUN ["apt-get", "update"]
#RUN ["apt-get", "install", "-y", "vim"]
COPY . .
ENV FLASK_APP=app
