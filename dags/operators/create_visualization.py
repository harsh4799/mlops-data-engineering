import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)

def visualize_class_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(x='fraud', data=df)
    plt.title('Class Distribution')
    file_path = '/tmp/class_distribution.png'
    plt.savefig(file_path)
    plt.close()
    return file_path

def visualize_distance_from_home(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['distance_from_home'], kde=True)
    plt.title('Distance from Home Distribution')
    file_path = '/tmp/distance_from_home.png'
    plt.savefig(file_path)
    plt.close()
    return file_path

def visualize_distance_from_last_transaction(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['distance_from_last_transaction'], kde=True)
    plt.title('Distance from Last Transaction Distribution')
    file_path = '/tmp/distance_from_last_transaction.png'
    plt.savefig(file_path)
    plt.close()
    return file_path

def visualize_ratio_to_median_purchase_price(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['ratio_to_median_purchase_price'], kde=True)
    plt.title('Ratio to Median Purchase Price Distribution')
    file_path = '/tmp/ratio_to_median_purchase_price.png'
    plt.savefig(file_path)
    plt.close()
    return file_path

def visualize_categorical_columns(df, column):
    plt.figure(figsize=(10, 6))
    sns.countplot(x=column, data=df)
    plt.title(f'{column.replace("_", " ").title()} Distribution')
    file_path = f'/tmp/{column}_distribution.png'
    plt.savefig(file_path)
    plt.close()
    return file_path

def visualization_composer(df, ti):
    visualization_steps = {
        "class_distribution_visualization": visualize_class_distribution,
        "distance_from_home_visualization": visualize_distance_from_home,
        "distance_from_last_transaction_visualization": visualize_distance_from_last_transaction,
        "ratio_to_median_purchase_price_visualization": visualize_ratio_to_median_purchase_price,
    }

    # Add visualizations for categorical columns
    categorical_columns = ['repeat_retailer', 'used_chip', 'used_pin_number', 'online_order', 'fraud']
    for column in categorical_columns:
        visualization_steps[f"{column}_visualization"] = lambda df, col=column: visualize_categorical_columns(df, col)

    for step_name, step_function in visualization_steps.items():
        visualization_path = step_function(df)
        ti.xcom_push(key=step_name, value=visualization_path)

def create_visualizations(**kwargs):
    ti = kwargs['ti']
    data_json = ti.xcom_pull(key='credit_card_data', task_ids='extract_data')
    df = pd.read_json(data_json)
    visualization_composer(df, ti)
