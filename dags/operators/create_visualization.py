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
    return file_path

def visualization_composer(df, ti):
    visualization_steps = {
        "class_distribution_visualization": visualize_class_distribution,
    }
    for step_name, step_function in visualization_steps.items():
        visualization_path = step_function(df)
        ti.xcom_push(key=step_name, value=visualization_path)

def create_visualizations(**kwargs):
    ti = kwargs['ti']
    data_json = ti.xcom_pull(key='credit_card_data', task_ids='extract_data')
    df = pd.read_json(data_json)
    visualization_composer(df, ti)
