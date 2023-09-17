import pandas as pd
import time
import boto3
from datetime import date
#
TABLE_NAME = "aba-get-house-listing"
DATE_FORMAT = "%Y-%m-%d"

dynamodb_client = boto3.client("dynamodb")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

today = date.today().strftime(DATE_FORMAT)

houses_batch = []

def get_price_int(price):
    return int(price.replace('€', '').strip().replace(' ', ''))

def load_item_csv(csv):
    df = pd.read_csv(csv, dtype=str, header=0, index_col=False)
    item_csv_data = df.to_dict('index')
    return item_csv_data

def write_batch(houses):
    with table.batch_writer() as writer:
        for house in houses:
            writer.put_item(Item=house)

def construct_item(house_info):
    return {
        "agence_name": house_info['agence_name'],
        "house_id": house_info['house_id'],
        "house_url": house_info['house_url'],
        "house_value": str(get_price_int(house_info['house_value'])),
        "date_created": today,
        "date_modified": today,
        "date_deleted": "",
        "house_status": "New",
        }

def put_new_item(item):
    response = dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item=item
    )
    return response

item_csv_data = load_item_csv('tmp/demeures_normandes_scrape.csv')

for _, house_info in item_csv_data.items():
    houses_batch.append(construct_item(house_info))

print(houses_batch[0])

# put_new_item(houses_batch[0])

write_batch(houses_batch)
