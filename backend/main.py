from logger_config import logger, tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.event_handler.exceptions import NotFoundError, BadRequestError
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, Field, ValidationError
import dynamo

app = APIGatewayHttpResolver()

class StatusRequest(BaseModel):
    parcel_id: str = Field(pattern=r"^DYN\d{9}$")
    email: str = Field(pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    phone: str = Field(pattern=r"^\+?[1-9]\d{1,14}$")

class StatusResponse(BaseModel):
    parcel_id: str
    status: str

@app.post("/parcel/status")
@tracer.capture_method
def get_parcel_status():
    body = app.current_event.json_body or {}

    if not body:
        logger.warning("Received empty request body - possible bot activity")
        raise BadRequestError("Invalid input format")
    try:
        data = StatusRequest(**body)
    except (ValidationError, TypeError):
        logger.warning("Input validation failed - bypassed frontend or bot")
        raise BadRequestError("Invalid input format")

    item = dynamo.get_parcel(data.parcel_id, data.email, data.phone)

    if not item:
        raise NotFoundError("Parcel not found")

    return StatusResponse(**item).model_dump()


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)