import pandas as pd
import time 
import boto3

dynamodb_client = boto3.client("dynamodb")
TABLE_NAME = "aba-get-house-listing"

#
item_csv_data = {}

def load_item_csv(csv):
    df = pd.read_csv(csv, header=0, index_col=1)
    item_csv_data = df.to_dict('index')
    return item_csv_data

def load_item_db():
    # Use the DynamoDB client to query for all songs by artist Arturus Ardvarkian
    response = dynamodb_client.query(
    TableName=TABLE_NAME,
    KeyConditionExpression='agence_name = :agence_name',
    ExpressionAttributeValues={
        ':agence_name': {'S': 'century'}
    })
    print(response['Items'])

def put_new_item(item):
    response = dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item=item
    )
    return response

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

# load_item_csv('tmp/agences.demeures_normandes_scrape.csv')
load_item_db()

# for item in items:
#     put_new_item(item)
#     time.sleep(1)