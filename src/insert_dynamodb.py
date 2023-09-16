import boto3

dynamodb_client = boto3.client("dynamodb")

table_name = "aba-get-house-listing"

def put_item_in_DB(item):
    response = dynamodb_client.put_item(
        TableName=table_name,
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

put_item_in_DB('test')
