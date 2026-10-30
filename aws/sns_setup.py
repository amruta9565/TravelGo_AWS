"""
TravelGo - Amazon SNS Topic Setup Script
Creates 'travelgo-booking-alerts' topic and optionally subscribes an admin/user email.
"""

import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

REGION = os.getenv("AWS_REGION", "us-east-1")
TOPIC_NAME = "travelgo-booking-alerts"


def setup_sns_topic(notification_email=None):
    sns = boto3.client("sns", region_name=REGION)
    print(f"Creating/retrieving SNS topic '{TOPIC_NAME}' in {REGION}...")

    try:
        response = sns.create_topic(Name=TOPIC_NAME)
        topic_arn = response["TopicArn"]
        print(f"✅ SNS Topic ready: {topic_arn}")

        if notification_email:
            print(f"Subscribing email '{notification_email}' to topic...")
            sub_res = sns.subscribe(
                TopicArn=topic_arn,
                Protocol="email",
                Endpoint=notification_email
            )
            print(f"Subscription initiated. SubscriptionArn: {sub_res.get('SubscriptionArn')}")
            print("⚠️ Check your email inbox to confirm the AWS SNS subscription!")

        print("\nSet this in your production .env or EC2 environment:")
        print(f"SNS_BOOKING_TOPIC_ARN={topic_arn}")
        return topic_arn

    except ClientError as e:
        print(f"❌ Error setting up SNS: {e}")
        raise


if __name__ == "__main__":
    import sys
    email = sys.argv[1] if len(sys.argv) > 1 else None
    setup_sns_topic(email)
