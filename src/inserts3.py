import boto3

# boto3.setup_default_session(profile_name="ah")

dynamodb_client = boto3.client("dynamodb")

table_name = "aba-get-house-listing"

response = dynamodb_client.put_item(
    TableName=table_name,
    Item={
        "house_id": {"S": "6934937708"},
        "agence_name": {"S": "agences.century"},
        "house_url": {"S": "https://www.century21.fr/trouver_logement/detail/6934937708/"},
        "house_value": {"N": "264000"},
    },
)
print(response)