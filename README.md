## Parcel Data Pipeline (AWS Serverless)

Serverless data pipeline for ingesting and processing parcel tracking data. The architecture uses a dual-storage setup to support both fast API lookups and relational queries.

## Core Architecture

The flow is event-driven, starting with S3 triggers that invoke Dockerized Python Lambdas. These handle normalization and risk classification, with an optional OpenAI fallback for handling unknown status values (controlled via USE_AI_CLASSIFIER).

    Storage: Data is written to DynamoDB (low-latency API access) and PostgreSQL/SQLAlchemy (relational queries).
    API: Exposed via API Gateway with Pydantic validation for incoming requests.

## DevOps

    Observability: Logging, tracing, and metrics using AWS Lambda Powertools.
    Infra: Managed via Terraform with CI/CD via GitHub Actions.

Env Vars: DB_URL, TABLE_NAME, OPENAI_API_KEY, USE_AI_CLASSIFIER.

Stack: Python, AWS (S3, Lambda, DynamoDB, API Gateway), PostgreSQL, Docker, Terraform.