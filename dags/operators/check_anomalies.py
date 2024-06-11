import pandas as pd
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv('config/.env')

def detect_anomalies(df):
    mean_distance_from_home = df['distance_from_home'].mean()
    std_distance_from_home = df['distance_from_home'].std()
    threshold = 3  

    anomalies = df[(df['distance_from_home'] > mean_distance_from_home + threshold * std_distance_from_home) |
                   (df['distance_from_home'] < mean_distance_from_home - threshold * std_distance_from_home)]
    return anomalies

def send_email(anomalies_df):
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL')

    sender_email = smtp_user

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Anomaly Detection Alert'

    body = f"Anomalies have been detected in the credit card transactions:\n\n{anomalies_df.to_string(index=False)}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
        logger.info("Anomaly detection email sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

def check_anomalies(ti):
    data_json = ti.xcom_pull(key='credit_card_data', task_ids='extract_data')
    df = pd.read_json(data_json)

    anomalies_df = detect_anomalies(df)
    if not anomalies_df.empty:
        logger.warning("Anomalies detected!")
        send_email(anomalies_df)
        return True
    else:
        logger.info("No anomalies detected.")
        return False

