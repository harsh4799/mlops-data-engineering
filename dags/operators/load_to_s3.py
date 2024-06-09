import boto3
import os
import pandas as pd
from dotenv import load_dotenv
import yaml
from airflow.models import TaskInstance
from airflow.utils.db import provide_session
from airflow.models import XCom
from enum import Enum
import logging

logger = logging.getLogger(__name__)


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

class xcom_type(Enum):
    DATA = 1
    TABLE = 2
    VISUALIZATION = 3

def check_xcom_type(xcom_key):
    if 'data' in xcom_key:
        return xcom_type.DATA
    elif 'table' in xcom_key:
        return xcom_type.TABLE
    elif 'visualization' in xcom_key:
        return xcom_type.VISUALIZATION
    else:
        return None

@provide_session
def get_all_xcoms(dag_id, execution_date, session=None):
    results = session.query(XCom).filter(XCom.dag_id == dag_id, XCom.execution_date == execution_date).all()
    return results


def load_to_s3(**kwargs):

    with open('config/s3_config.yaml') as file:
        s3_config = yaml.safe_load(file)
    s3_bucket = s3_config['bucket_name']

    ti = kwargs['ti']
    dag_id = ti.dag_id
    execution_date = ti.execution_date

    xcoms = get_all_xcoms(dag_id, execution_date)

    # Upload all XCom files to S3 based on their category
    for xcom in xcoms:
        key = xcom.key
        value = xcom.value
        category = check_xcom_type(key)
        
        logger.info("Processing ", key, " of category ", category)

        if category == xcom_type.VISUALIZATION:
            s3_client.upload_file(value, s3_bucket, f'visualizations/{os.path.basename(value)}')
        elif category == xcom_type.TABLE:
            table_data = pd.read_json(value)
            table_path = f'/tmp/{key}.csv'
            table_data.to_csv(table_path, index=False)
            s3_client.upload_file(table_path, s3_bucket, f'tables/{os.path.basename(table_path)}')
        elif category == xcom_type.DATA:
            continue