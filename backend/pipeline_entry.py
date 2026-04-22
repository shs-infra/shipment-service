from logger_config import logger, tracer
from pipeline_service import run_pipeline
from aws_lambda_powertools import Metrics

metrics = Metrics(namespace="ParcelPipeline")

@metrics.log_metrics
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    logger.info("Pipeline triggered", extra={"event": event})

    try:
        run_pipeline(event)
    except Exception as e:
        logger.exception("Pipeline execution failed", extra={"error": str(e)})
        raise

    return {"status": "ok"}