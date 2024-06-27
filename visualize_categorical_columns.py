import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns

def visualize_categorical_columns(categorical_columns = ['repeat_retailer', 'used_chip', 'used_pin_number', 'online_order', 'fraud'], **kwargs):

    ti = kwargs['ti']
    data_json = ti.xcom_pull(key='credit_card_data', task_ids='extract_data')
    df = pd.read_json(data_json)
    for column in categorical_columns:
        plt.figure(figsize=(10, 6))
        sns.countplot(x=column, data=df)
        plt.title(f'{column.replace("_", " ").title()} Distribution')
        file_path = f'/tmp/{column}_distribution.png'
        plt.savefig(file_path)
        plt.close()
        ti.xcom_push(key=f"{column}_visualization", value=file_path)
        