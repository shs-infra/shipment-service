import os
import boto3
from botocore.exceptions import ClientError
from logger_config import logger, tracer

TABLE_NAME = os.environ.get("TABLE_NAME")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

@tracer.capture_method
def get_parcel(parcel_id: str, email: str, phone: str) -> dict | None:

    tracer.put_annotation(key="parcel_id", value=parcel_id)
    tracer.put_metadata(key="debug_info", value={"email": email, "phone": phone})

    try:
        response = table.get_item(Key={"parcel_id": parcel_id})
        item = response.get("Item")

        if item:

            tracer.put_metadata(key="db_record", value={
                "email": item.get("email"), 
                "phone": item.get("phone")
            })
            
            if item.get("email") == email and item.get("phone") == phone:
                tracer.put_annotation(key="search_result", value="SUCCESS")
                return item
        
            logger.debug("Data mismatch detected for parcel", extra={"parcel_id": parcel_id})

            logger.warning("Auth mismatch for existing record", extra={"parcel_id": parcel_id})

            tracer.put_annotation(key="search_result", value="MISMATCH")

            return None

        tracer.put_annotation(key="search_result", value="NOT_FOUND")

        return None

    except ClientError as e:
        tracer.put_annotation(key="search_result", value="TECHNICAL_ERROR")
        error_code = e.response["Error"]["Code"]
        logger.exception(
            "DynamoDB get_item failed",
            extra={
                "parcel_id": parcel_id,
                "aws_error_code": error_code
            }
        )
        raise

def save_parcel(parcel: dict) -> None:
    parcel_id = parcel.get("parcel_id")

    try:
        table.put_item(Item=parcel)

        logger.info(
            "Parcel saved to DynamoDB",
            extra={"parcel_id": parcel_id}
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        logger.exception(
            "DynamoDB put_item failed",
            extra={
                "parcel_id": parcel_id,
                "aws_error_code": error_code
            }
        )

        raise