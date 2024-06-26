from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from operators import perform_eda,extract_data, visualize_categorical_columns, load_to_s3, check_anomalies, visualize_ratio_to_median_purchase_price
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
}

dag = DAG(
    'fraud_detection_dag',
    default_args=default_args,
    description='A DAG for credit card fraud detection pipeline',
    schedule_interval=timedelta(days=28),
    start_date=days_ago(1),
    catchup=False,
)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

eda_task = PythonOperator(
    task_id='perform_eda',
    python_callable=perform_eda,
    provide_context=True,
    dag=dag,
)

visualize_categorical_columns_task = PythonOperator(
    task_id='visualize_categorical_columns',
    python_callable=visualize_categorical_columns,
    provide_context=True,
    dag=dag,
)

visualize_ratio_to_median_purchase_price_task = PythonOperator(
    task_id='visualize_ratio_to_median_purchase_price',
    python_callable=visualize_ratio_to_median_purchase_price,
    provide_context=True,
    dag=dag,
)


check_anomalies_task = PythonOperator(
    task_id='check_anomalies',
    python_callable = check_anomalies,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_s3',
    python_callable=load_to_s3,
    dag=dag,
)

extract_task >> check_anomalies_task >> [eda_task, visualize_categorical_columns_task, visualize_ratio_to_median_purchase_price_task] >> load_task
# extract_task >> [eda_task, visualization_task] >> load_task

