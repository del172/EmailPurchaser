from __future__ import annotations

import re
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Iterable, List

PURCHASE_KEYWORDS_STRONG = [
    r"invoice",
    r"receipt",
    r"payment received",
    r"payment confirmation",
    r"charged",
    r"transaction (?:id|number)",
    r"order confirmation",
    r"purchase confirmation",
    r"tax invoice",
]

PURCHASE_KEYWORDS_WEAK = [
    r"order",
    r"purchase",
    r"shipped",
    r"shipping confirmation",
    r"thank you for your order",
]

EXCLUSION_KEYWORDS = [
    r"offer",
    r"promo",
    r"promotion",
    r"deal",
    r"sale",
    r"discount",
    r"newsletter",
    r"coupon",
    r"limited time",
    r"new arrivals",
    r"clearance",
    r"unsubscribe",
]

AMOUNT_PATTERNS = [
    r"\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?",
    r"\btotal\s*(?:amount)?\s*[:\-]?\s*\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})?",
]

REFERENCE_PATTERNS = [
    r"(invoice|order|receipt|transaction)\s*(?:#|no\.|number)?\s*[a-z0-9-]{3,}",
    r"\bconfirmation\s*(?:#|no\.|number)?\s*[a-z0-9-]{3,}",
]


def _matches(text: str, patterns: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered) for pattern in patterns)


def _has_transaction_marker(text: str) -> bool:
    return _matches(text, AMOUNT_PATTERNS) or _matches(text, REFERENCE_PATTERNS)


def is_purchase_email(email: Dict[str, Any]) -> bool:
    """Return True if the email content looks like a purchase or invoice."""

    subject = email.get("subject", "")
    body = email.get("snippet", "")
    text = f"{subject}\n{body}".lower()

    has_promo_language = _matches(text, EXCLUSION_KEYWORDS)
    has_strong_signal = _matches(text, PURCHASE_KEYWORDS_STRONG)
    has_weak_signal = _matches(text, PURCHASE_KEYWORDS_WEAK)
    has_transaction_marker = _has_transaction_marker(text)

    if has_promo_language and not has_strong_signal:
        return False

    if has_strong_signal:
        return True

    return has_weak_signal and has_transaction_marker


def filter_purchase_emails(emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    purchases: List[Dict[str, Any]] = []
    for email in emails:
        if is_purchase_email(email):
            purchases.append(_normalize_email(email))
    return sorted(purchases, key=lambda e: e.get("date") or datetime.min, reverse=True)


def _normalize_email(email: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(email)
    date_value = email.get("date")
    if isinstance(date_value, str):
        try:
            normalized["date"] = datetime.fromisoformat(date_value)
        except ValueError:
            normalized["date"] = None
    return normalized


def summarize_purchases(purchases: List[Dict[str, Any]]) -> Dict[str, Any]:
    vendor_counts = defaultdict(int)
    total_spent = 0.0
    for purchase in purchases:
        vendor = purchase.get("from", "Unknown Vendor")
        vendor_counts[vendor] += 1
        amount = purchase.get("total")
        if amount is not None:
            try:
                total_spent += float(amount)
            except (TypeError, ValueError):
                continue

    return {
        "count": len(purchases),
        "total_spent": total_spent,
        "vendors": dict(sorted(vendor_counts.items(), key=lambda item: item[1], reverse=True)),
    }
