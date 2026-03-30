# Cloud Integration & Serverless Data Pipeline

Serverless data pipeline on AWS for processing and exposing parcel tracking data.

## Overview

This project implements an end-to-end pipeline that ingests parcel data, processes and enriches it, applies classification logic, and exposes results via a REST API. The system is designed using AWS serverless services and containerized Lambda functions.

## Architecture

A scheduled EventBridge trigger invokes a pipeline Lambda function, which processes incoming parcel data and stores it in DynamoDB for fast API access and PostgreSQL for analytical queries. A separate Lambda function serves as an API layer behind API Gateway, enabling real-time parcel status retrieval.

## Processing

Raw data is transformed into a structured format through a Python-based processing layer. This includes normalization of fields, enrichment with timestamps, and classification of parcel status. Classification is implemented using a hybrid approach combining rule-based logic with optional AI-based fallback using OpenAI.

## Deployment

The system uses two separate Docker-based Lambda functions. One handles API requests, while the other is responsible for scheduled data processing. This separation ensures clear responsibility boundaries and scalability.

## Scheduling

The pipeline is executed automatically using Amazon EventBridge with a configurable schedule, for example every five minutes.

## Configuration

Environment variables are used to configure database connections, API keys, and feature flags such as enabling or disabling AI-based classification.

## Example

The API accepts a parcel ID along with user credentials and returns the current parcel status. Data is validated and retrieved from DynamoDB with low latency.

## Tech Stack

AWS Lambda, API Gateway, DynamoDB, PostgreSQL, EventBridge, Python, Docker, SQLAlchemy, OpenAI API.

## Design

The system separates ingestion, processing, and API layers, uses a hybrid classification approach, and combines NoSQL and SQL relational storage to balance performance and analytical capabilities.