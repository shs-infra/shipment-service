from logger_config import logger
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, NotFoundError
from aws_lambda_powertools.utilities.typing import LambdaContext
import dynamo

app = APIGatewayHttpResolver()

@app.get("/parcel/<parcel_id>")
def get_parcel_route(parcel_id: str):
    item = dynamo.get_parcel(parcel_id)

    if not item:
        logger.info("Parcel not found", extra={"parcel_id": parcel_id, "http_status": 404})
        raise NotFoundError(f"Parcel {parcel_id} not found")

    return item


@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)