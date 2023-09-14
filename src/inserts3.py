import boto3

dynamodb_client = boto3.client("dynamodb", region_name='eu-west-1')

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

try:
    table.put_item(
        Item={
            'foo':1,
            'bar':2,
        },
        ConditionExpression='attribute_not_exists(foo) AND attribute_not_exists(bar)'
    )
except botocore.exceptions.ClientError as e:
    # Ignore the ConditionalCheckFailedException, bubble up
    # other exceptions.
    if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
        raise