import json
import boto3
from processor import process_parcel
from db_sql import save_parcel as save_sql
from dynamo import save_parcel as save_dynamo
from logger_config import logger
from aws_lambda_powertools import Metrics

metrics = Metrics(namespace="ParcelPipeline")

s3 = boto3.client("s3")


def load_from_s3(bucket: str, key: str):
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response["Body"].read().decode("utf-8")
    return json.loads(content)


def run_pipeline(event: dict):
    records = event.get("Records", [])

    if not records:
        logger.warning("No records in event")
        return

    for record in records:
        process_record(record)


def process_record(record: dict):
    try:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        if not key.endswith(".json"):
            logger.warning("Skipping non-JSON file", extra={"key": key})
            return

        logger.info("Processing file", extra={"bucket": bucket, "key": key})

        raw_data = load_from_s3(bucket, key)

        process_batch(raw_data)

    except Exception as e:
        logger.exception("Failed to process record", extra={"error": str(e)})
        raise


def process_batch(raw_data: list[dict]):
    if not isinstance(raw_data, list):
        raise ValueError("Invalid data format: expected list")

    metrics.add_metric(name="BatchProcessed", unit="Count", value=1)
    metrics.add_metric(name="BatchSize", unit="Count", value=len(raw_data))

    for raw in raw_data:
        try:
            processed = process_parcel(raw)

            logger.info("Processed parcel", extra=processed)

            metrics.add_metric(name="ProcessedParcels", unit="Count", value=1)

            if processed["risk_level"] == "high":
                metrics.add_metric(name="HighRiskParcels", unit="Count", value=1)

            save_sql(processed)
            save_dynamo(processed)

            metrics.add_metric(name="SavedParcels", unit="Count", value=1)

        except Exception as e:
            logger.exception(
                "Failed to process parcel",
                extra={"raw": raw, "error": str(e)}
            )

            metrics.add_metric(name="FailedParcels", unit="Count", value=1)