import pandas as pd

def eda_describe(df):
    return df.describe()

def eda_composer(df, ti):
    eda_steps = {"Describe_table":eda_describe,}
    for eda_step in eda_steps.keys():
        eda_results = eda_steps[eda_step](df)
        ti.xcom_push(key=eda_step, value=eda_results.to_json())

def perform_eda(**kwargs):
    ti = kwargs['ti']
    data_json = ti.xcom_pull(key='credit_card_data', task_ids='extract_data')
    df = pd.read_json(data_json)
    eda_composer(df,ti)
   