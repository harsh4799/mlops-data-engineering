import boto3
import pandas as pd
from io import StringIO
import yaml
from dotenv import load_dotenv
import os


# dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv('config/.env')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def extract_data(**kwargs):
    with open('config/s3_config.yaml') as file:
        s3_config = yaml.safe_load(file)
    obj = s3_client.get_object(Bucket=s3_config['bucket_name'], Key=s3_config['object_key'])
    data = obj['Body'].read().decode('utf-8')
    df = pd.read_csv(StringIO(data))
    kwargs['ti'].xcom_push(key='credit_card_data', value=df.to_json())
