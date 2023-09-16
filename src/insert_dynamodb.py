import boto3

dynamodb_client = boto3.client("dynamodb")

table_name = "aba-get-house-listing"

response = dynamodb_client.put_item(
    TableName=table_name,
    Item={
        "house_id": "111-350174",
        "agence_name": "agences.demeures_normandes",
        "house_url": "https://auxdemeuresnormandes.com/property/maison-de-174-m%c2%b2-a-15-mn-de-vernon/",
        "house_value": 350000,
        "date_created": "2023-09-16",
        "date_modified": "",
        "date_deleted": "",
    },
)