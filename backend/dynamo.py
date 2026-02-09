import os
import boto3
from botocore.exceptions import ClientError
from logger_config import logger

TABLE_NAME = os.environ.get("TABLE_NAME")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def get_parcel(parcel_id: str) -> dict | None:
    
    try:
        response = table.get_item(Key={"parcel_id": parcel_id})
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        metadata = e.response["ResponseMetadata"]

        logger.exception(
            "DynamoDB get_item failed",
            extra={
                "aws_error_code": error_code,
                "aws_request_id": metadata["RequestId"],
                "http_status": metadata["HTTPStatusCode"],
                "operation": "get_item"
            }
        )
        raise

    return response.get("Item")