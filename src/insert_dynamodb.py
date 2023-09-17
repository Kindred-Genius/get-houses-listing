import pandas as pd
import time
import boto3
from datetime import date


dynamodb_client = boto3.client("dynamodb")
TABLE_NAME = "aba-get-house-listing"
DATE_FORMAT = "%Y-%m-%d"

today = date.today().strftime(DATE_FORMAT)

def key_missing(dict, key):
    if key in dict.keys(): return False
    else: return True

def get_price_int(price):
    return int(price.replace('€', '').strip().replace(' ', ''))

def load_item_csv(csv):
    df = pd.read_csv(csv, dtype=str, header=0, index_col=1)
    df.index = df.index.astype(str)
    item_csv_data = df.to_dict('index')
    return item_csv_data

def load_item_db(table, primary_value):
    # Use the DynamoDB client to query for all songs by artist Arturus Ardvarkian
    response = dynamodb_client.query(
    TableName=table,
    KeyConditionExpression='agence_name = :agence_name',
    ExpressionAttributeValues={
        ':agence_name': {'S': primary_value}
    })
    return response['Items']

def process_db_response(db_response):
    item_db_data = {}
    for item in db_response:
        key = item['house_id']['S']
        value = item['house_value']['N']
        item_db_data[key] = value
    return item_db_data

def compare_db_csv_data(item_csv_data, item_db_data):
    for house_id, house_info in item_csv_data.items():
        house_value = get_price_int(house_info['house_value'])
        if key_missing(item_db_data, house_id):
            print(house_id, ': does not exist , new item')
            new_item = construct_item(house_id, house_info)
            put_new_item(new_item)
            time.sleep(0.5)
        elif house_value != int(item_db_data[house_value]):
            print(house_id, ': exist but price different')
            updated_item = construct_updated_item(house_info)
            update_house(house_id, house_info['agence_name'], updated_item)
            time.sleep(0.5)
    for house_id in item_db_data.keys():
        if key_missing(item_csv_data, house_id):
            print(house_id, ': item deleted')
            deleted_item = construct_deleted_item()
            update_house(house_id, house_info['agence_name'], deleted_item)
            time.sleep(0.5)

def construct_item(house_id, house_info):
    return {
        "agence_name": {"S": house_info['agence_name']},
        "house_id": {"S": str(house_id)},
        "house_url": {"S": house_info['house_url']},
        "house_value": {"N": str(get_price_int(house_info['house_value']))},
        "date_created": {"S": today},
        "date_modified": {"S": today},
        "date_deleted": {"S": ""},
        "house_status": {"S": "New"},
        }

def construct_updated_item(house_info):
    return {
        ":house_value": {"N": str(get_price_int(house_info['house_value']))},
        ":date_modified": {"S": today},
        ":house_status": {"S": "Price update"},
        }

def construct_deleted_item():
    return {
        ":date_deleted": {"S": today},
        ":house_status": {"S": "Deleted"},
        }

def put_new_item(item):
    response = dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item=item
    )
    return response

def update_house(house_id, agence_name, updated_item):
    expression = [f'{key[1:]}={key}' for key in updated_item.keys()]
    print(f'set {", ".join(expression)}')
    response = dynamodb_client.update_item(
        TableName=TABLE_NAME,
        Key={'agence_name': {"S": agence_name}, 'house_id': {"S": house_id}},
        UpdateExpression=f'set {", ".join(expression)}',
        ExpressionAttributeValues=updated_item,
        ReturnValues="UPDATED_NEW")
    return response['Attributes']



item_csv_data = load_item_csv('tmp/agences.century_scrape.ori.csv')
item_db_data = load_item_db(table=TABLE_NAME, primary_value='century')

compare_db_csv_data(item_csv_data, item_db_data)

# for item in items:
#     put_new_item(item)
#     time.sleep(1)

db_response =[{
    'date_modified': {'S': '2023-09-17'}, 'house_url': {'S': 'https://www.century21.fr/trouver_logement/detail/6603199178/'}, 'house_id': {'S': '6603199178'}, 'date_deleted': {'S': ''}, 'date_created': {'S': '2023-09-17'},
     'agence_name': {'S': 'century'}, 'house_value': {'N': '528000'}}, {'date_modified': {'S': '2023-09-17'}, 'house_url': {'S': 'https://www.century21.fr/trouver_logement/detail/6934937708/'}, 'house_id': {'S': '6934937708'}, 'date_deleted': {'S': ''}, 'date_created': {'S': '2023-09-17'}, 'agence_name': {'S': 'century'}, 'house_value': {'N': '264000'}
    }]

items = [{
            "agence_name": {"S": "century"},
            "house_id": {"S": "6934937708"},
            "house_url": {"S": "https://www.century21.fr/trouver_logement/detail/6934937708/"},
            "house_value": {"N": "264000"},
            "date_created": {"S": "2023-09-17"},
            "date_modified": {"S": "2023-09-17"},
            "date_deleted": {"S": ""},
        },
        {
            "agence_name": {"S": "century"},
            "house_id": {"S": "6603199178"},
            "house_url": {"S": "https://www.century21.fr/trouver_logement/detail/6603199178/"},
            "house_value": {"N": "528000"},
            "date_created": {"S": "2023-09-17"},
            "date_modified": {"S": "2023-09-17"},
            "date_deleted": {"S": ""},
        },
        {
            "agence_name": {"S": "demeures_normandes"},
            "house_id": {"S": "111-350174"},
            "house_url": {"S": "https://auxdemeuresnormandes.com/property/maison-de-174-m%c2%b2-a-15-mn-de-vernon/"},
            "house_value": {"N": "350000"},
            "date_created": {"S": "2023-09-16"},
            "date_modified": {"S": ""},
            "date_deleted": {"S": ""},
        }]
