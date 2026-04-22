import os
from openai import OpenAI
from logger_config import logger

USE_AI = os.environ.get("USE_AI_CLASSIFIER", "false").lower() == "true"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

HIGH_RISK = {"DELAYED", "FAILED", "LOST"}
MEDIUM_RISK = {"IN_TRANSIT", "OUT_FOR_DELIVERY"}

KNOWN_STATUSES = HIGH_RISK | MEDIUM_RISK | {"DELIVERED"}


def classify(status: str) -> str:

    status = status.upper()

    if status in HIGH_RISK:
        return "high"

    if status in MEDIUM_RISK:
        return "medium"

    if status == "DELIVERED":
        return "low"

    if status not in KNOWN_STATUSES and USE_AI:
        try:
            return classify_with_ai(status)
        except Exception as e:
            logger.warning("AI classification failed, fallback to default", extra={"status": status, "error": str(e)})

    return "medium"


def classify_with_ai(status: str) -> str:

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify parcel delivery risk.\n"
                    "Return ONLY one word: low, medium, or high.\n"
                    "High = delivery problems, delays, failures.\n"
                    "Medium = still in progress.\n"
                    "Low = successfully delivered."
                )
            },
            {
                "role": "user",
                "content": f"Status: {status}"
            }
        ],
        temperature=0,
        timeout=2
    )

    result = response.choices[0].message.content.strip().lower()

    if result not in {"low", "medium", "high"}:
        raise ValueError(f"Invalid AI response: {result}")

    return result