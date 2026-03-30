from datetime import datetime
from classifier import classify

def normalize_status(status: str) -> str:
    return status.lower()

def process_parcel(raw: dict) -> dict:
    return {
        "parcel_id": raw["id"],
        "status": raw["status"],
        "status_normalized": normalize_status(raw["status"]),
        "risk_level": classify(raw["status"]),
        "processed_at": datetime.utcnow().isoformat(),
        "email": "test@test.com",
        "phone": "+48123456789"
    }