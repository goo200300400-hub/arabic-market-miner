import csv
import io
import re
import unicodedata
from collections import Counter
from urllib.parse import urlparse

import requests
from apify import Actor

PURCHASE_PATTERNS = [
    "بكم", "كم السعر", "السعر", "أريد شراء", "ابغى اشتري", "ابي اشتري",
    "كيف اطلب", "طريقة الطلب", "متوفر", "وين احصل", "من وين", "اطلب",
    "اشتري", "شراء", "buy", "price", "how much", "where can i buy",
    "available", "order", "purchase"
]
COMPLAINT_PATTERNS = [
    "سيء", "سيئ", "مشكلة", "ما اشتغل", "لا يعمل", "خرب", "تالف",
    "تأخر", "متأخر", "غالي", "سعره مرتفع", "جودة", "رديء",
    "لم يصل", "ما وصل", "خدمة سيئة", "شكوى", "bad", "broken",
    "doesn't work", "not working", "problem", "late", "expensive",
    "poor quality", "damaged", "complaint"
]
REQUEST_PATTERNS = [
    "أتمنى", "يا ريت", "نحتاج", "احتاج", "ياليت", "لو توفر",
    "غير موجود", "أريد", "ممكن توفر", "wish", "need", "please add",
    "not available", "i want"
]

def normalize(text):
    text = unicodedata.normalize("NFKC", str(text or "")).lower()
    text = re.sub(r"[إأآا]", "ا", text)
    text = re.sub(r"[ىي]", "ي", text)
    text = re.sub(r"[\u064b-\u065f\u0670]", "", text)
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def matches(text, patterns):
    normalized = normalize(text)
    return [p for p in patterns if normalize(p) in normalized]

def analyze(comment):
    text = str(comment or "").strip()
    purchase = matches(text, PURCHASE_PATTERNS)
    complaints = matches(text, COMPLAINT_PATTERNS)
    requests = matches(text, REQUEST_PATTERNS)
    categories = []
    if purchase:
        categories.append("purchase_intent")
    if complaints:
        categories.append("complaint")
    if requests:
        categories.append("product_request")
    if not categories:
        categories.append("general")
    return {
        "comment": text,
        "categories": categories,
        "purchase_intent": bool(purchase),
        "complaint": bool(complaints),
        "product_request": bool(requests),
        "matched_purchase_terms": purchase,
        "matched_complaint_terms": complaints,
        "matched_request_terms": requests,
    }

def read_csv_url(url, column_name):
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("csv_url must be a public http/https URL.")
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    response.encoding = response.encoding or "utf-8-sig"
    reader = csv.DictReader(io.StringIO(response.text))
    if not reader.fieldnames:
        raise ValueError("The CSV file has no header row.")
    candidates = [column_name, "comment", "text", "تعليق", "التعليق"]
    selected = next((name for name in candidates if name and name in reader.fieldnames), None)
    if not selected:
        raise ValueError(
            "Could not find a comment column. Set column_name to the CSV column, "
            "or use one of: comment, text, تعليق, التعليق."
        )
    return [row.get(selected, "") for row in reader]

async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        comments = actor_input.get("comments") or []
        csv_url = actor_input.get("csv_url")
        column_name = actor_input.get("column_name", "comment")

        if csv_url:
            comments = read_csv_url(csv_url, column_name)
        if isinstance(comments, str):
            comments = [comments]
        if not isinstance(comments, list) or not comments:
            raise ValueError("Provide a non-empty 'comments' array or a public 'csv_url'.")

        results = [analyze(item) for item in comments if str(item or "").strip()]
        if not results:
            raise ValueError("No non-empty comments were found.")

        summary = {
            "total_comments": len(results),
            "purchase_intent_count": sum(r["purchase_intent"] for r in results),
            "complaint_count": sum(r["complaint"] for r in results),
            "product_request_count": sum(r["product_request"] for r in results),
            "general_count": sum("general" in r["categories"] for r in results),
            "top_complaint_terms": Counter(
                term for r in results for term in r["matched_complaint_terms"]
            ).most_common(10),
            "top_purchase_terms": Counter(
                term for r in results for term in r["matched_purchase_terms"]
            ).most_common(10),
            "method_note": "Rule-based keyword matching; results are indicators, not verified buying decisions or sentiment analysis."
        }

        await Actor.push_data({"record_type": "summary", **summary})
        for result in results:
            await Actor.push_data({"record_type": "comment_analysis", **result})
        Actor.log.info(
            "Analyzed %s comments: %s purchase-intent indicators, %s complaints.",
            len(results), summary["purchase_intent_count"], summary["complaint_count"]
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
