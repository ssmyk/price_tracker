from bs4 import BeautifulSoup
import requests
from datetime import datetime
from celery import Celery
from celery.exceptions import Ignore

celery_beat_schedule = {
    "time_scheduler": {"task": "app.scraper.run_update", "schedule": 30.0}
}

celery_app = Celery(
    "tasks",
    backend="rpc://",
    broker="amqp://guest:guest@rabbitmq//",
    beat_schedule=celery_beat_schedule,
)


@celery_app.task(default_retry_delay=1, max_retries=None)
def run_update():
    requests.get("http://scraper_api:5500/api/")


@celery_app.task(bind=True, default_retry_delay=1, max_retries=None)
def scraper_task_add(self, asin: str, user_id: str):
    page_url = f"https://www.amazon.pl/dp/{asin}"
    page = requests.get(page_url, timeout=None)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        product_details = {}
        product_details["name"] = soup.title.string.split(":")[0]
        product_details["price"] = float(
            soup.find(id="tp_price_block_total_price_ww")
            .get_text()
            .split("zł")[0]
            .replace("\xa0", "")
            .replace(",", ".")
        )
        product_details["image"] = soup.find(id="landingImage")["data-old-hires"]
        product_details["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        product_details["asin"] = asin
        product_details["user_id"] = user_id

        resp = create_product_request(product_details)
        status_code = resp.status_code
        new_status = task_status_update(status_code)
        self.update_state(state=new_status)
        raise Ignore()
    else:
        self.retry()


def create_product_request(product_details: dict) -> requests.models.Response:
    resp = requests.post(
        "http://web_app:5000/products/",
        json={
            "product_name": product_details["name"],
            "product_image": product_details["image"],
            "product_asin": product_details["asin"],
            "date_added": product_details["date"],
            "current_price": product_details["price"],
            "current_price_date": product_details["date"],
            "lowest_price": product_details["price"],
            "lowest_price_date": product_details["date"],
            "fk_user": product_details["user_id"],
        },
    )
    return resp


def task_status_update(status_code: int) -> str:
    statuses = {409: "DUPLICATE", 201: "CREATED", 500: "ERROR"}
    return statuses.get(status_code)


@celery_app.task(bind=True, default_retry_delay=1, max_retries=None)
def scraper_task_update(self, asin: str, user_id: str):
    page_url = f"https://www.amazon.pl/dp/{asin}"
    page = requests.get(page_url, timeout=None)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")

        product_details = {}
        product_details["price"] = float(
            soup.find(id="tp_price_block_total_price_ww")
            .get_text()
            .split("zł")[0]
            .replace("\xa0", "")
            .replace(",", ".")
        )
        product_details["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        product_details["user_id"] = user_id
        product_details["asin"] = asin
        update_product_request(product_details)
        return f'Current price for {asin}: {product_details["price"]} PLN'
    else:
        self.retry()


def update_product_request(product_details: dict) -> None:
    requests.post(
        "http://web_app:5000/products/update/",
        json={
            "product_asin": product_details["asin"],
            "date": product_details["date"],
            "price": product_details["price"],
            "fk_user": product_details["user_id"],
        },
    )