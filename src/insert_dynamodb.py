import pandas as pd
import boto3

dynamodb_client = boto3.client("dynamodb")
TABLE_NAME = "aba-get-house-listing"

#
item_csv_data = {}

def load_item_csv(csv):
    df = pd.read_csv(csv, header=0, index_col=1)
    item_csv_data = df.to_dict('index')
    return item_csv_data

def load_item_db(test):
    response = dynamodb_client.query(
        TableName=TABLE_NAME,
        KeyConditionExpression='house_id = :house_id AND agence_name = :agence_name',
        ExpressionAttributeValues={
            ':house_id': {'S': '*'},
            ':agence_name': {'S': 'agences.demeures_normandes'}
        }
    )
    print(response['Items'])

def put_new_item(item):
    response = dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item={
            "house_id": {"S": "111-350174"},
            "agence_name": {"S": "agences.demeures_normandes"},
            "house_url": {"S": "https://auxdemeuresnormandes.com/property/maison-de-174-m%c2%b2-a-15-mn-de-vernon/"},
            "house_value": {"N": "350000"},
            "date_created": {"S": "2023-09-16"},
            "date_modified": {"S": ""},
            "date_deleted": {"S": ""},
        },
    )

load_item_db('tmp/agences.demeures_normandes_scrape.csv')
