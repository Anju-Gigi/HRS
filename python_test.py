import os
import csv
import json
import boto3
import redis
import pandas as pd
from io import StringIO
from datetime import datetime

# Load environment variables
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

S3_BUCKET = os.getenv('S3_BUCKET')
S3_REGION = os.getenv('S3_REGION', 'eu-north-1')

# Connect to Redis
redis_client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

# Connect to S3
s3_client = boto3.client('s3', region_name=S3_REGION)

def fetch_redis_data():
    """Fetch all keys and their values from Redis."""
    keys = redis_client.keys('*')
    data = []
    for key in keys:
        value = redis_client.get(key)
        data.append({'key': key, 'value': value})
    return data

def export_to_csv(data):
    """Export data to CSV format."""
    df = pd.DataFrame(data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def export_to_json(data):
    """Export data to JSON format."""
    return json.dumps(data)

def upload_to_s3(data, file_format):
    """Upload data to S3."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    if file_format == 'csv':
        filename = f'redis_data_{timestamp}.csv'
        s3_client.put_object(Bucket=S3_BUCKET, Key=filename, Body=data)
    elif file_format == 'json':
        filename = f'redis_data_{timestamp}.json'
        s3_client.put_object(Bucket=S3_BUCKET, Key=filename, Body=data)

def main():
    data = fetch_redis_data()

    # Export to CSV and upload to S3
    csv_data = export_to_csv(data)
    upload_to_s3(csv_data, 'csv')

    # Export to JSON and upload to S3
    json_data = export_to_json(data)
    upload_to_s3(json_data, 'json')

if __name__ == '__main__':
    main()
