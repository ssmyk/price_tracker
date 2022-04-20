# Amazon Price Tracker

# Table of contents

* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Application view](#application-view)

## General info

The application allows you to track the prices of amazon.pl products. Through the implemented user registration and
login system, it is possible to track prices by many users simultaneously.

## Technologies

* Python 3.10
* Flask 2.1.1
* Celery 5.2.6
* RabbitMQ 3.10.0
* Beautiful Soup 4.11.1
* WTForms 3.0.1
* Celery 5.2.6
* PostgreSQL 14
* Docker 20.10.14
* Docker Compose 2.4.1

## Setup

1. Create `.env` files.  
   &nbsp;  
   There are below `.env_default` files:  
   ```
   price_tracker\.env_default
   price_tracker\web_app\app\.env_default
   price_tracker\scraper_api\app_\.env_default
   ```
   Rename them to `.env`. You may change constants like `SECRET_KEY` to your own values.  
   &nbsp;
2. Build and run containers.  
   &nbsp;  
   Inside program folder run in CMD:  
   `docker compose up --build`  
   &nbsp;
3. Migrate database.  
   &nbsp;  
   Open CLI in web_app container and run:  
   `flask db init`  
   &nbsp;  
   Go to folder /web_app/migration and put inside file `env.py`:   
   `from app.models import Users, Models`  
   &nbsp;  
   Run in CLI:  
   `flask db migrate`  
   `flask db upgrade`  
   &nbsp;
4. The application should be ready to use:   
   `http://localhost:5000`

## Application view

![price_tracker](https://user-images.githubusercontent.com/72394779/163056004-a508c403-7f7c-420b-97bb-8a60e26bbbc7.gif)

## Architecture diagram

![price_tracker](https://user-images.githubusercontent.com/72394779/164174706-e099d0b4-db54-4124-aa2f-c066f303ef1d.png)
