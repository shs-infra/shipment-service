from data_source import get_parcel_data
from processor import process_parcel
from db_sql import save_parcel as save_sql
from dynamo import save_parcel as save_dynamo
from logger_config import logger, tracer


@tracer.capture_lambda_handler
def lambda_handler(event, context):
    logger.info("Pipeline started")

    raw_data = get_parcel_data()

    for raw in raw_data:
        processed = process_parcel(raw)

        logger.info("Processed parcel", extra=processed)

        save_sql(processed)
        save_dynamo(processed)

    logger.info("Pipeline finished")

    return {"status": "ok"}