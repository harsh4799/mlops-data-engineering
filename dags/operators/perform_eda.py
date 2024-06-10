import pandas as pd
import io 
import logging

logger = logging.getLogger(__name__)

def eda_describe(df):
    return df.describe()

# def eda_info(df):
#     return df.dtypes.reset_index()

def eda_missing_values(df):
    return df.isnull().sum().reset_index()

def eda_composer(df, ti):
    eda_steps = {
                    "Describe_table": eda_describe, 
                    # "Info_table": eda_info, 
                    "Missing_Values_table": eda_missing_values
                }

    for eda_step in eda_steps.keys():
        logger.critical("eda_step",eda_step)
        eda_results = eda_steps[eda_step](df)
        ti.xcom_push(key=eda_step, value=eda_results.to_json())

def perform_eda(**kwargs):
    ti = kwargs['ti']
    data_json = ti.xcom_pull(key='credit_card_data', task_ids='extract_data')
    df = pd.read_json(data_json)
    eda_composer(df,ti)
