from flask import Flask


def create_api() -> Flask:
    app = Flask(__name__)
    from .views import ScraperAPI, TaskStatus

    app.add_url_rule(
        "/api/", view_func=ScraperAPI.as_view("scraper_api"), methods=["PATCH", "POST"]
    )
    app.add_url_rule(
        "/status/<task_id>", view_func=TaskStatus.as_view("status"), methods=["GET"]
    )
    return app
