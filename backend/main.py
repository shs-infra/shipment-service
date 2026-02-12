from logger_config import logger
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.event_handler.exceptions import NotFoundError, BadRequestError
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, Field, ValidationError
import dynamo

app = APIGatewayHttpResolver()

class ParcelRequest(BaseModel):
    parcel_id: str = Field(pattern=r"^DYN\d{9}$")

@app.get("/parcel/<parcel_id>")
def get_parcel_route(parcel_id: str):

    try:
        req = ParcelRequest(parcel_id=parcel_id)
    except ValidationError:
        raise BadRequestError(f"Invalid parcel_id format. Expected DYN followed by 9 digits")

    item = dynamo.get_parcel(req.parcel_id)

    if not item:
        logger.info("Parcel not found", extra={"parcel_id": req.parcel_id, "http_status": 404})
        raise NotFoundError(f"Parcel {req.parcel_id} not found")

    return item


@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)