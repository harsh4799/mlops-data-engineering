import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns

def visualize_distance_from_home(**kwargs):
    ti = kwargs['ti']
    data_json = ti.xcom_pull(key='credit_card_data', task_ids='extract_data')
    df = pd.read_json(data_json)

    plt.figure(figsize=(10, 6))
    sns.histplot(df['distance_from_home'], kde=True)
    plt.title('Distance from Home Distribution')
    file_path = '/tmp/distance_from_home.png'
    plt.savefig(file_path)
    plt.close()
    ti.xcom_push(key=f"distance_from_home_visualization", value=file_path)