import os
from sqlalchemy import create_engine, text

engine = create_engine(os.environ.get("DB_URL"))


def save_parcel(parcel: dict):
    query = text("""
        INSERT INTO parcels (
            parcel_id, status, status_normalized, risk_level, processed_at
        )
        VALUES (:parcel_id, :status, :status_normalized, :risk_level, :processed_at)
    """)

    with engine.connect() as conn:
        conn.execute(query, parcel)
        conn.commit()