from datetime import datetime, timedelta
from typing import Any, Dict, List


def fetch_emails() -> List[Dict[str, Any]]:
    """Return a mock set of Gmail messages for demonstration purposes.

    In a production app this function would authenticate with Gmail and
    fetch the latest messages. The data below simulates a mix of purchase
    confirmations and promotional offers so the filtering logic can be
    exercised without external credentials.
    """

    now = datetime.utcnow()
    return [
        {
            "id": "1",
            "subject": "Your order has shipped - Invoice #12345",
            "snippet": "Thanks for shopping with us. Here is your receipt for $48.99.",
            "from": "Acme Supplies",
            "date": (now - timedelta(hours=2)).isoformat(),
            "total": 48.99,
        },
        {
            "id": "2",
            "subject": "Limited time offer: 30% off summer styles",
            "snippet": "Don't miss this promo for the weekend only!",
            "from": "Fashion Hub",
            "date": (now - timedelta(days=1)).isoformat(),
            "total": None,
        },
        {
            "id": "3",
            "subject": "Payment received for your subscription renewal",
            "snippet": "We have processed your payment of $12.00 for the next month.",
            "from": "Streamly",
            "date": (now - timedelta(days=2, hours=3)).isoformat(),
            "total": 12.00,
        },
        {
            "id": "4",
            "subject": "Order confirmation - #ABCD77889",
            "snippet": "Your purchase of wireless earbuds is confirmed.",
            "from": "Audio World",
            "date": (now - timedelta(days=3)).isoformat(),
            "total": 89.50,
        },
        {
            "id": "5",
            "subject": "Promo newsletter - deals you can't miss",
            "snippet": "This week's coupons and discounts are here.",
            "from": "SuperSaver",
            "date": (now - timedelta(days=4)).isoformat(),
            "total": None,
        },
        {
            "id": "6",
            "subject": "Invoice for your recent stay",
            "snippet": "Attached is your hotel invoice with a total of $210.75.",
            "from": "City Hotel",
            "date": (now - timedelta(days=6)).isoformat(),
            "total": 210.75,
        },
    ]
