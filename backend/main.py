from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
app = APIGatewayHttpResolver()

@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)