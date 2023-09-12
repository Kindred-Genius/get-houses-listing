import boto3
import os
from datetime import date

def get_today_date():
    todays = date.today()
    return todays.year, todays.month, todays.day 

def put_csv_s3():
    bucket_name = 'aba-get-house-listing'
    path = 'tmp/'
    year, month, day = get_today_date()
    s3 = boto3.resource('s3')

    for subdir, dirs, files in os.walk(path):
        for file in files:
            s3.meta.client.upload_file(f'{path}{file}', bucket_name, f'{year}/{month}/{day}/{file}')

    # Deleting files from tmp
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

if __name__ == "__main__":
    put_csv_s3()
