import os
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger("travelgo.db")

# Path to local persistent store for mock mode
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
LOCAL_DB_FILE = DATA_DIR / "local_db.json"


class DynamoDBService:
    """
    DynamoDB Data Access Service with seamless Local Mock fallback.
    Ensures the platform works out-of-the-box locally, while supporting
    production AWS DynamoDB when AWS credentials/EC2 roles are provided.
    """

    def __init__(self, app_config=None):
        self.use_mock = True
        self.region = "us-east-1"
        self.users_table_name = "travelgo_users"
        self.bookings_table_name = "travelgo_bookings"
        self.dynamodb = None
        self.users_table = None
        self.bookings_table = None

        if app_config:
            self.init_app(app_config)
        else:
            self._init_local_store()

    def init_app(self, config):
        self.use_mock = config.get("USE_MOCK_AWS", True)
        self.region = config.get("AWS_REGION", "us-east-1")
        self.users_table_name = config.get("DYNAMODB_USERS_TABLE", "travelgo_users")
        self.bookings_table_name = config.get("DYNAMODB_BOOKINGS_TABLE", "travelgo_bookings")

        if not self.use_mock:
            try:
                import boto3
                self.dynamodb = boto3.resource("dynamodb", region_name=self.region)
                self.users_table = self.dynamodb.Table(self.users_table_name)
                self.bookings_table = self.dynamodb.Table(self.bookings_table_name)
                logger.info("Connected to AWS DynamoDB in region %s", self.region)
            except Exception as e:
                logger.warning("Could not connect to AWS DynamoDB: %s. Falling back to local mock store.", e)
                self.use_mock = True

        if self.use_mock:
            self._init_local_store()

    def _init_local_store(self):
        """Initializes local JSON store with initial sample data."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not LOCAL_DB_FILE.exists():
            default_data = {
                "users": {},
                "bookings": {}
            }
            self._save_local_store(default_data)

    def _load_local_store(self):
        try:
            if LOCAL_DB_FILE.exists():
                with open(LOCAL_DB_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            logger.error("Error reading local DB file: %s", e)
        return {"users": {}, "bookings": {}}

    def _save_local_store(self, data):
        try:
            with open(LOCAL_DB_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error("Error saving local DB file: %s", e)

    # ---------------- USER OPERATIONS ----------------

    def create_user(self, user_dict):
        """Saves a new user record."""
        user_dict["created_at"] = datetime.now(timezone.utc).isoformat()
        if not self.use_mock and self.users_table:
            try:
                self.users_table.put_item(Item=user_dict)
                return user_dict
            except Exception as e:
                logger.error("DynamoDB put_item user error: %s", e)
                raise

        # Local mock mode
        store = self._load_local_store()
        store["users"][user_dict["email"].lower()] = user_dict
        self._save_local_store(store)
        return user_dict

    def get_user_by_email(self, email):
        """Fetches user record by email."""
        if not email:
            return None
        email_clean = email.strip().lower()

        if not self.use_mock and self.users_table:
            try:
                res = self.users_table.get_item(Key={"email": email_clean})
                return res.get("Item")
            except Exception as e:
                logger.error("DynamoDB get_user_by_email error: %s", e)
                return None

        # Local mock mode
        store = self._load_local_store()
        return store["users"].get(email_clean)

    def get_user_by_id(self, user_id):
        """Fetches user record by user_id."""
        if not user_id:
            return None

        if not self.use_mock and self.users_table:
            try:
                # Query index or scan
                res = self.users_table.scan(
                    FilterExpression="user_id = :uid",
                    ExpressionAttributeValues={":uid": user_id}
                )
                items = res.get("Items", [])
                return items[0] if items else None
            except Exception as e:
                logger.error("DynamoDB scan user by id error: %s", e)

        store = self._load_local_store()
        for user in store["users"].values():
            if user.get("user_id") == user_id:
                return user
        return None

    # ---------------- BOOKING OPERATIONS ----------------

    def create_booking(self, booking_dict):
        """Creates a booking record."""
        booking_dict["created_at"] = datetime.now(timezone.utc).isoformat()
        booking_dict["status"] = booking_dict.get("status", "CONFIRMED")

        if not self.use_mock and self.bookings_table:
            try:
                self.bookings_table.put_item(Item=booking_dict)
                return booking_dict
            except Exception as e:
                logger.error("DynamoDB put_item booking error: %s", e)
                raise

        # Local mock mode
        store = self._load_local_store()
        store["bookings"][booking_dict["booking_id"]] = booking_dict
        self._save_local_store(store)
        return booking_dict

    def get_booking_by_id(self, booking_id):
        """Fetches booking by booking_id."""
        if not booking_id:
            return None

        if not self.use_mock and self.bookings_table:
            try:
                res = self.bookings_table.get_item(Key={"booking_id": booking_id})
                return res.get("Item")
            except Exception as e:
                logger.error("DynamoDB get_booking_by_id error: %s", e)
                return None

        store = self._load_local_store()
        return store["bookings"].get(booking_id)

    def get_user_bookings(self, user_id):
        """Returns all bookings associated with user_id, sorted by travel date."""
        if not user_id:
            return []

        bookings = []
        if not self.use_mock and self.bookings_table:
            try:
                res = self.bookings_table.scan(
                    FilterExpression="user_id = :uid",
                    ExpressionAttributeValues={":uid": user_id}
                )
                bookings = res.get("Items", [])
            except Exception as e:
                logger.error("DynamoDB scan user bookings error: %s", e)
        else:
            store = self._load_local_store()
            bookings = [b for b in store["bookings"].values() if b.get("user_id") == user_id]

        # Sort descending by travel_date
        bookings.sort(key=lambda x: x.get("travel_date", ""), reverse=True)
        return bookings

    def cancel_booking(self, booking_id, user_id):
        """Cancels a booking if it belongs to the user and is CONFIRMED."""
        booking = self.get_booking_by_id(booking_id)
        if not booking:
            return False, "Booking not found."

        if booking.get("user_id") != user_id:
            return False, "Unauthorized access to this booking."

        if booking.get("status") == "CANCELLED":
            return False, "This booking has already been cancelled."

        updated_at = datetime.now(timezone.utc).isoformat()

        if not self.use_mock and self.bookings_table:
            try:
                self.bookings_table.update_item(
                    Key={"booking_id": booking_id},
                    UpdateExpression="SET #s = :status, cancelled_at = :time",
                    ExpressionAttributeNames={"#s": "status"},
                    ExpressionAttributeValues={":status": "CANCELLED", ":time": updated_at}
                )
                booking["status"] = "CANCELLED"
                booking["cancelled_at"] = updated_at
                return True, booking
            except Exception as e:
                logger.error("DynamoDB cancel_booking error: %s", e)
                return False, str(e)

        # Local mock mode
        store = self._load_local_store()
        if booking_id in store["bookings"]:
            store["bookings"][booking_id]["status"] = "CANCELLED"
            store["bookings"][booking_id]["cancelled_at"] = updated_at
            self._save_local_store(store)
            return True, store["bookings"][booking_id]

        return False, "Failed to update booking status."


# Global singleton instance
db = DynamoDBService()
