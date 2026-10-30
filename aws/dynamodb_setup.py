"""
TravelGo - Amazon DynamoDB Table Setup Script
Creates 'travelgo_users' and 'travelgo_bookings' tables with proper keys and indexes.
"""

import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

REGION = os.getenv("AWS_REGION", "us-east-1")
USERS_TABLE = os.getenv("DYNAMODB_USERS_TABLE", "travelgo_users")
BOOKINGS_TABLE = os.getenv("DYNAMODB_BOOKINGS_TABLE", "travelgo_bookings")


def get_dynamodb_client():
    return boto3.client("dynamodb", region_name=REGION)


def create_users_table(dynamodb):
    print(f"Creating DynamoDB table: {USERS_TABLE}...")
    try:
        table = dynamodb.create_table(
            TableName=USERS_TABLE,
            KeySchema=[
                {"AttributeName": "email", "KeyType": "HASH"}  # Partition key
            ],
            AttributeDefinitions=[
                {"AttributeName": "email", "AttributeType": "S"},
                {"AttributeName": "user_id", "AttributeType": "S"}
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "UserIdIndex",
                    "KeySchema": [
                        {"AttributeName": "user_id", "KeyType": "HASH"}
                    ],
                    "Projection": {"ProjectionType": "ALL"}
                }
            ],
            BillingMode="PAY_PER_REQUEST"  # On-Demand pricing
        )
        print(f"Waiting for {USERS_TABLE} to become ACTIVE...")
        waiter = dynamodb.get_waiter("table_exists")
        waiter.wait(TableName=USERS_TABLE)
        print(f"✅ {USERS_TABLE} created successfully!")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"ℹ️ Table {USERS_TABLE} already exists.")
        else:
            print(f"❌ Error creating {USERS_TABLE}: {e}")
            raise


def create_bookings_table(dynamodb):
    print(f"Creating DynamoDB table: {BOOKINGS_TABLE}...")
    try:
        table = dynamodb.create_table(
            TableName=BOOKINGS_TABLE,
            KeySchema=[
                {"AttributeName": "booking_id", "KeyType": "HASH"}  # Partition key
            ],
            AttributeDefinitions=[
                {"AttributeName": "booking_id", "AttributeType": "S"},
                {"AttributeName": "user_id", "AttributeType": "S"}
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "UserBookingsIndex",
                    "KeySchema": [
                        {"AttributeName": "user_id", "KeyType": "HASH"}
                    ],
                    "Projection": {"ProjectionType": "ALL"}
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        print(f"Waiting for {BOOKINGS_TABLE} to become ACTIVE...")
        waiter = dynamodb.get_waiter("table_exists")
        waiter.wait(TableName=BOOKINGS_TABLE)
        print(f"✅ {BOOKINGS_TABLE} created successfully!")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"ℹ️ Table {BOOKINGS_TABLE} already exists.")
        else:
            print(f"❌ Error creating {BOOKINGS_TABLE}: {e}")
            raise


if __name__ == "__main__":
    print(f"Connecting to DynamoDB in region {REGION}...")
    client = get_dynamodb_client()
    create_users_table(client)
    create_bookings_table(client)
    print("\n🎉 DynamoDB provisioning complete!")
