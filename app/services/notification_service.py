import logging
from datetime import datetime, timezone

logger = logging.getLogger("travelgo.sns")


class NotificationService:
    """
    AWS Simple Notification Service (SNS) Service for booking and cancellation alerts.
    Gracefully falls back to mock console/in-memory logging when in local development.
    """

    def __init__(self, app_config=None):
        self.use_mock = True
        self.region = "us-east-1"
        self.topic_arn = None
        self.sns_client = None
        self.sent_notifications = []  # In-memory history for testing and verification

        if app_config:
            self.init_app(app_config)

    def init_app(self, config):
        self.use_mock = config.get("USE_MOCK_AWS", True)
        self.region = config.get("AWS_REGION", "us-east-1")
        self.topic_arn = config.get("SNS_BOOKING_TOPIC_ARN", "")

        if not self.use_mock and self.topic_arn:
            try:
                import boto3
                self.sns_client = boto3.client("sns", region_name=self.region)
                logger.info("Configured AWS SNS client for topic %s", self.topic_arn)
            except Exception as e:
                logger.warning("Could not initialize AWS SNS client: %s. Using local mock notifier.", e)
                self.use_mock = True

    def send_booking_confirmation(self, booking_data, user_email):
        """Sends booking confirmation email via AWS SNS."""
        subject = f"✈️ TravelGo Confirmation: Booking #{booking_data.get('booking_id')} Confirmed"
        
        mode = booking_data.get("service_type", "").capitalize()
        title = booking_data.get("item_title", "Trip")
        travel_date = booking_data.get("travel_date", "Upcoming")
        total_price = booking_data.get("total_amount", 0.0)
        passenger_name = booking_data.get("passenger_name", "Traveler")
        seats = booking_data.get("seats", [])
        seat_str = f"Seats: {', '.join(seats)}\n" if seats else ""

        message = f"""
============================================================
              TRAVELGO BOOKING CONFIRMATION
============================================================
Hello {passenger_name},

Thank you for choosing TravelGo! Your booking has been confirmed.

BOOKING DETAILS:
------------------------------------------------------------
Booking ID   : {booking_data.get('booking_id')}
Service Type : {mode}
Item / Route : {title}
Travel Date  : {travel_date}
{seat_str}Total Paid   : ${total_price:.2f}
Status       : CONFIRMED
Created At   : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

You can view, download, or manage your reservation anytime in your TravelGo Dashboard:
http://travelgo.internal/dashboard

Safe travels!
The TravelGo Team
============================================================
"""
        return self._publish(subject, message, user_email, alert_type="CONFIRMATION")

    def send_cancellation_confirmation(self, booking_data, user_email):
        """Sends booking cancellation email via AWS SNS."""
        subject = f"⚠️ TravelGo Notice: Booking #{booking_data.get('booking_id')} Cancelled"

        message = f"""
============================================================
              TRAVELGO BOOKING CANCELLATION
============================================================
Hello {booking_data.get('passenger_name', 'Traveler')},

Your booking #{booking_data.get('booking_id')} has been successfully CANCELLED.

CANCELLATION SUMMARY:
------------------------------------------------------------
Booking ID    : {booking_data.get('booking_id')}
Service Type  : {booking_data.get('service_type', '').capitalize()}
Trip / Hotel  : {booking_data.get('item_title')}
Travel Date   : {booking_data.get('travel_date')}
Refund Status : Refund of ${booking_data.get('total_amount', 0):.2f} initiated
Status        : CANCELLED
Cancelled At  : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

If you have any questions, please visit your TravelGo dashboard or contact support.

Thank you,
The TravelGo Team
============================================================
"""
        return self._publish(subject, message, user_email, alert_type="CANCELLATION")

    def _publish(self, subject, message, recipient_email, alert_type="GENERAL"):
        record = {
            "subject": subject,
            "message": message,
            "recipient": recipient_email,
            "alert_type": alert_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "delivered": False
        }

        if not self.use_mock and self.sns_client and self.topic_arn:
            try:
                response = self.sns_client.publish(
                    TopicArn=self.topic_arn,
                    Subject=subject[:100],  # SNS subjects max 100 chars
                    Message=message,
                    MessageAttributes={
                        "Email": {
                            "DataType": "String",
                            "StringValue": recipient_email
                        },
                        "Type": {
                            "DataType": "String",
                            "StringValue": alert_type
                        }
                    }
                )
                record["delivered"] = True
                record["sns_message_id"] = response.get("MessageId")
                logger.info("SNS published successfully. MessageId: %s", response.get("MessageId"))
            except Exception as e:
                logger.error("SNS publish error: %s", e)
                record["error"] = str(e)
        else:
            # Local mock notification logging
            record["delivered"] = True
            record["mock"] = True
            logger.info("[MOCK AWS SNS] Email notification dispatched to %s: %s", recipient_email, subject)

        self.sent_notifications.append(record)
        return record


# Global singleton instance
notification_service = NotificationService()
