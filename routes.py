from datetime import datetime
from typing import Any, Dict, List
from flask import Flask, render_template

from services.email_processor import filter_purchase_emails, summarize_purchases
from services.gmail_service import fetch_emails


def register_routes(app: Flask) -> None:
    @app.route("/")
    def dashboard() -> str:
        raw_emails: List[Dict[str, Any]] = fetch_emails()
        purchases = filter_purchase_emails(raw_emails)
        summary = summarize_purchases(purchases)

        return render_template(
            "dashboard.html",
            purchases=purchases,
            summary=summary,
            last_refreshed=datetime.utcnow(),
        )
