import pandas as pd
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import os
from email import encoders

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

    body = "Anomalies have been detected in the credit card transactions. Please find the attached CSV file for details."
    msg.attach(MIMEText(body, 'plain'))

    # Save the DataFrame to a CSV file
    csv_filename = "anomalies.csv"
    anomalies_df.to_csv(csv_filename, index=False)

    # Attach the CSV file
    with open(csv_filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {csv_filename}",
        )
        msg.attach(part)

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



if __name__=="__main__":
    send_email(pd.DataFrame.from_dict({"Vibe":["Check"]}))