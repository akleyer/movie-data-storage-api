"""Interacts with the DynamoDB database for movie management."""

import os
import boto3
from botocore.exceptions import ClientError

# Configure the DynamoDB client
dynamodb_client = boto3.client(
    'dynamodb',
    endpoint_url=os.getenv('DYNAMODB_ENDPOINT', 'http://dynamodb-local:8000'),
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'fakeMyKeyId'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'fakeSecretAccessKey')
)

def create_movies_table(dynamodb_client):
    """
    Creates the Movies table in DynamoDB with year (HASH) and title (RANGE) as keys.

    Args:
        dynamodb_client (boto3.client): The DynamoDB client object.

    Returns:
        None
    """

    table = dynamodb_client.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    # Wait for the table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName='Movies')
    app.logger.info(f"Created Movies table with provisioned throughput: ReadCapacityUnits={10}, WriteCapacityUnits={10}")

def check_and_create_movies_table():
    """
    Checks if the Movies table exists in DynamoDB and creates it if not.

    Returns:
        None
    """

    existing_tables = dynamodb_client.list_tables()['TableNames']
    if 'Movies' not in existing_tables:
        print("Movies table does not exist, creating...")
        create_movies_table(dynamodb_client)
    else:
        print("Movies table already exists.")

def get_movies_from_db(app, year, title, cast_member, genre):
    """
    Retrieves movies from the Movies table based on optional filter parameters.

    Args:
        year (str, optional): Filter movies by release year.
        title (str, optional): Filter movies by title (exact match).
        cast_member (str, optional): Filter movies by cast member name (exact match).
        genre (str, optional): Filter movies by genre.

    Returns:
        tuple:
            - list: List of movie items retrieved from the database.
            - str: Empty string if successful, error message otherwise.
    """

    app.logger.info(f"Retrieving movies from the Movies table with filters: year={year}, title={title}, cast_member={cast_member}, genre={genre}")

    # Construct the filter expression
    filter_expressions = []
    expression_attribute_names = {}
    expression_attribute_values = {}

    if year:
        filter_expressions.append("#yr = :year")  # Use #yr as a placeholder for 'year'
        expression_attribute_names["#yr"] = "year"  # Map #yr to the actual attribute name 'year'
        expression_attribute_values[":year"] = {"N": str(year)}

    if title:
        filter_expressions.append("contains (title, :title)")
        expression_attribute_values[":title"] = {"S": title}

    if cast_member:
        filter_expressions.append("contains (#cst, :cast)")
        expression_attribute_names["#cst"] = "cast"  # Substitute #cst to represent 'cast'
        expression_attribute_values[":cast"] = {"S": cast_member}

    if genre:
        filter_expressions.append("contains (genres, :genre)")
        expression_attribute_values[":genre"] = {"S": genre}

    # Combine all filter expressions
    combined_filter_expression = " AND ".join(filter_expressions) if filter_expressions else None

    try:
        # Perform the scan operation
        scan_kwargs = {
            "TableName": "Movies",
            "ExpressionAttributeValues": expression_attribute_values
        }

        # Add the FilterExpression if there are filters
        if combined_filter_expression:
            scan_kwargs["FilterExpression"] = combined_filter_expression

        # Add ExpressionAttributeNames if needed
        if expression_attribute_names:
            scan_kwargs["ExpressionAttributeNames"] = expression_attribute_names

        response = dynamodb_client.scan(**scan_kwargs)

        # Extract items from response
        items = response.get('Items', [])
        
        app.logger.debug(f"Retrieved {len(items)} movies from the database")
        return items, ""

    except ClientError as e:
        app.logger.error(f"Error scanning Movies table: {str(e)}")
        return [], str(e)
