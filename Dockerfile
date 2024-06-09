FROM apache/airflow:2.8.0

# Install any custom python packages
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt