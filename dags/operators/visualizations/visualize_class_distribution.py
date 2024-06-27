import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns

def visualize_class_distribution(**kwargs):
    ti = kwargs['ti']
    data_json = ti.xcom_pull(key='credit_card_data', task_ids='extract_data')

    df = pd.read_json(data_json)
    plt.figure(figsize=(10, 6))
    sns.countplot(x='fraud', data=df)
    plt.title('Class Distribution')
    file_path = '/tmp/class_distribution.png'
    plt.savefig(file_path)
    plt.close()
    
    ti.xcom_push(key="class_distribution_visualization", value=file_path)
