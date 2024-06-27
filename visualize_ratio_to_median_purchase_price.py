import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns



def visualize_ratio_to_median_purchase_price(**kwargs):
    ti = kwargs['ti']
    data_json = ti.xcom_pull(key='credit_card_data', task_ids='extract_data')
    df = pd.read_json(data_json)

    plt.figure(figsize=(10, 6))
    sns.histplot(df['ratio_to_median_purchase_price'], kde=True)
    plt.title('Ratio to Median Purchase Price Distribution')
    file_path = '/tmp/ratio_to_median_purchase_price.png'
    plt.savefig(file_path)
    plt.close()
    ti.xcom_push(key=f"ratio_to_median_purchase_price_visualization", value=file_path)
        