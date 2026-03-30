import os
from openai import OpenAI
from logger_config import logger

USE_AI = os.environ.get("USE_AI_CLASSIFIER", "false").lower() == "true"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

HIGH_RISK = {"DELAYED", "FAILED", "LOST"}
MEDIUM_RISK = {"IN_TRANSIT", "OUT_FOR_DELIVERY"}


def classify(status: str) -> str:
    """
    Main classification entrypoint.
    Uses rule-based logic first, optionally falls back to AI.
    """

    status = status.upper()

    if status in HIGH_RISK:
        return "high"

    if status in MEDIUM_RISK:
        return "medium"

    if USE_AI:
        try:
            return classify_with_ai(status)
        except Exception as e:
            logger.warning("AI classification failed, fallback to default", extra={"error": str(e)})

    return "low"


def classify_with_ai(status: str) -> str:

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a logistics classifier. "
                    "Classify parcel status into one of: low, medium, high. "
                    "Respond with only one word."
                )
            },
            {
                "role": "user",
                "content": f"Parcel status: {status}"
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip().lower()

    if result not in {"low", "medium", "high"}:
        raise ValueError(f"Invalid AI response: {result}")

    return result