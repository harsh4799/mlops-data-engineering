# Airflow Data Pipeline

This repository contains an Apache Airflow data pipeline for a credit card fraud detection project. The pipeline extracts data from an S3 bucket, performs exploratory data analysis (EDA), creates visualizations, and loads the results back to S3.

## Getting Started

To get started with this project, follow the steps below:

### 1. Environment Setup

Create a `.env` file in the project root directory with the following environment variables:

```dotenv
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=your_aws_region
```

### 2. Running the Project

Start the project using Docker Compose:

```bash
docker-compose up
```

## Components

### 1. Extract Data

The `extract_data.py` script extracts data from an S3 bucket and passes it to the next task.

### 2. Perform EDA

The `perform_eda.py` script performs exploratory data analysis on the extracted data and pushes the EDA results to XCom.

### 3. Create Visualizations

The `create_visualizations.py` script generates visualizations based on the EDA results and uploads them to S3.

### 4. Load to S3

The `load_to_s3.py` script loads various data files, tables, visualizations, and EDA results to S3.

## Folder Structure

```
.
├── dags/
│   └── fraud_detection_dag.py
├── scripts/
│   ├── extract_data.py
│   ├── perform_eda.py
│   ├── create_visualizations.py
│   └── load_to_s3.py
├── config/
│   └── .env
├── Dockerfile
├── docker-compose.yaml
└── README.md
```
