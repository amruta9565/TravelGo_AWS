import uuid
from datetime import datetime, date, timedelta
from app.services.db_service import db
from app.services.notification_service import notification_service

# Predefined travel inventory catalog
BUS_INVENTORY = [
    {
        "id": "bus_101",
        "operator": "BlueArrow Express",
        "bus_type": "Luxury AC Sleeper (2+1)",
        "origin": "New York",
        "destination": "Boston",
        "departure_time": "08:00 AM",
        "arrival_time": "12:30 PM",
        "duration": "4h 30m",
        "price_per_seat": 45.0,
        "rating": 4.8,
        "amenities": ["WiFi", "Water Bottle", "Charging Point", "Reclining Seats"],
        "total_seats": 40,
        "booked_seats": ["1A", "1B", "3C", "4D", "6A", "10B"]
    },
    {
        "id": "bus_102",
        "operator": "MetroCruiser Premium",
        "bus_type": "Multi-Axle Semi-Sleeper AC",
        "origin": "New York",
        "destination": "Washington DC",
        "departure_time": "09:30 AM",
        "arrival_time": "02:15 PM",
        "duration": "4h 45m",
        "price_per_seat": 38.0,
        "rating": 4.6,
        "amenities": ["Air Conditioning", "WiFi", "USB Ports"],
        "total_seats": 40,
        "booked_seats": ["2A", "2B", "5A", "7C", "8D"]
    },
    {
        "id": "bus_103",
        "operator": "Pacific Coast Voyager",
        "bus_type": "Ultra Luxury Panoramic Coach",
        "origin": "San Francisco",
        "destination": "Los Angeles",
        "departure_time": "07:15 AM",
        "arrival_time": "01:45 PM",
        "duration": "6h 30m",
        "price_per_seat": 58.0,
        "rating": 4.9,
        "amenities": ["Panoramic Roof", "WiFi", "Snacks Included", "Entertainment Screen"],
        "total_seats": 40,
        "booked_seats": ["1A", "3B", "4A", "4B", "9C"]
    },
    {
        "id": "bus_104",
        "operator": "Midwest Star Line",
        "bus_type": "Executive AC Seater",
        "origin": "Chicago",
        "destination": "Detroit",
        "departure_time": "11:00 AM",
        "arrival_time": "03:45 PM",
        "duration": "4h 45m",
        "price_per_seat": 32.0,
        "rating": 4.4,
        "amenities": ["AC", "Charging Port", "Reading Light"],
        "total_seats": 40,
        "booked_seats": ["1B", "2C", "3D"]
    },
    {
        "id": "bus_105",
        "operator": "Emerald Cascades Shuttle",
        "bus_type": "Greenliner AC Executive",
        "origin": "Seattle",
        "destination": "Portland",
        "departure_time": "02:00 PM",
        "arrival_time": "05:30 PM",
        "duration": "3h 30m",
        "price_per_seat": 29.0,
        "rating": 4.7,
        "amenities": ["Eco-Hybrid", "High-speed WiFi", "Coffee Station"],
        "total_seats": 40,
        "booked_seats": ["3A", "3B", "5C"]
    }
]

TRAIN_INVENTORY = [
    {
        "id": "trn_201",
        "train_name": "Acela High-Speed Express",
        "train_number": "TR-2150",
        "origin": "New York",
        "destination": "Washington DC",
        "departure_time": "07:00 AM",
        "arrival_time": "09:55 AM",
        "duration": "2h 55m",
        "base_price": 85.0,
        "classes": [
            {"class_type": "Standard Coach", "price": 85.0, "available": 42},
            {"class_type": "Business Class", "price": 135.0, "available": 18},
            {"class_type": "First Class", "price": 210.0, "available": 6}
        ],
        "rating": 4.9,
        "amenities": ["Quiet Car", "Bistro Dining", "Ultra WiFi", "Extra Legroom"]
    },
    {
        "id": "trn_202",
        "train_name": "Northeast Regional",
        "train_number": "TR-176",
        "origin": "New York",
        "destination": "Boston",
        "departure_time": "08:30 AM",
        "arrival_time": "12:45 PM",
        "duration": "4h 15m",
        "base_price": 54.0,
        "classes": [
            {"class_type": "Standard Coach", "price": 54.0, "available": 55},
            {"class_type": "Business Class", "price": 98.0, "available": 24}
        ],
        "rating": 4.6,
        "amenities": ["Cafe Car", "Free WiFi", "Power Outlets"]
    },
    {
        "id": "trn_203",
        "train_name": "Coast Starlight Scenic",
        "train_number": "TR-14",
        "origin": "Los Angeles",
        "destination": "Seattle",
        "departure_time": "10:10 AM",
        "arrival_time": "08:30 PM",
        "duration": "34h 20m",
        "base_price": 120.0,
        "classes": [
            {"class_type": "Reserved Coach", "price": 120.0, "available": 30},
            {"class_type": "Superliner Roomette", "price": 340.0, "available": 8},
            {"class_type": "Bedroom Suite", "price": 620.0, "available": 3}
        ],
        "rating": 4.9,
        "amenities": ["Observation Lounge", "Full Dining Car", "Bedding & Shower"]
    },
    {
        "id": "trn_204",
        "train_name": "Lake Shore Limited",
        "train_number": "TR-48",
        "origin": "Chicago",
        "destination": "New York",
        "departure_time": "09:30 PM",
        "arrival_time": "06:25 PM",
        "duration": "19h 55m",
        "base_price": 95.0,
        "classes": [
            {"class_type": "Standard Coach", "price": 95.0, "available": 40},
            {"class_type": "Viewliner Roomette", "price": 285.0, "available": 10}
        ],
        "rating": 4.5,
        "amenities": ["Dining Services", "Reclining Seats", "Luggage Check"]
    }
]

FLIGHT_INVENTORY = [
    {
        "id": "flt_301",
        "airline": "SkyWing Airways",
        "flight_number": "SW-402",
        "origin": "New York",
        "origin_code": "JFK",
        "destination": "Los Angeles",
        "destination_code": "LAX",
        "departure_time": "06:45 AM",
        "arrival_time": "10:15 AM",
        "duration": "6h 30m",
        "stops": "Non-stop",
        "price": 245.0,
        "rating": 4.8,
        "cabin_class": "Economy",
        "amenities": ["In-flight Stream", "Complimentary Drink", "Carry-on 10kg", "Power at Seat"]
    },
    {
        "id": "flt_302",
        "airline": "AeroBlue Transcon",
        "flight_number": "AB-880",
        "origin": "New York",
        "origin_code": "EWR",
        "destination": "San Francisco",
        "destination_code": "SFO",
        "departure_time": "08:15 AM",
        "arrival_time": "11:50 AM",
        "duration": "6h 35m",
        "stops": "Non-stop",
        "price": 289.0,
        "rating": 4.9,
        "cabin_class": "Economy Plus",
        "amenities": ["Free High-Speed Viasat", "Live TV", "Snacks Included"]
    },
    {
        "id": "flt_303",
        "airline": "Continental Express",
        "flight_number": "CE-114",
        "origin": "Chicago",
        "origin_code": "ORD",
        "destination": "Miami",
        "destination_code": "MIA",
        "departure_time": "11:30 AM",
        "arrival_time": "03:40 PM",
        "duration": "3h 10m",
        "stops": "Non-stop",
        "price": 165.0,
        "rating": 4.5,
        "cabin_class": "Economy",
        "amenities": ["USB Charger", "Beverage Service"]
    },
    {
        "id": "flt_304",
        "airline": "Global Air",
        "flight_number": "GA-902",
        "origin": "San Francisco",
        "origin_code": "SFO",
        "destination": "Tokyo",
        "destination_code": "HND",
        "departure_time": "01:20 PM",
        "arrival_time": "05:10 PM",
        "duration": "11h 50m",
        "stops": "Non-stop",
        "price": 890.0,
        "rating": 4.9,
        "cabin_class": "International Economy",
        "amenities": ["2 Checked Bags", "Hot Meals", "Wide Touchscreen"]
    }
]

HOTEL_INVENTORY = [
    {
        "id": "htl_401",
        "name": "The Grand Azure Palace & Spa",
        "city": "New York",
        "location": "Midtown Manhattan, Central Park South",
        "category": "luxury",
        "stars": 5,
        "price_per_night": 380.0,
        "rating": 4.9,
        "reviews_count": 1420,
        "badge": "Luxury Signature",
        "amenities": ["Rooftop Heated Pool", "Full Service Spa", "Michelin Dining", "Valet Parking", "High-Speed WiFi", "Fitness Center"],
        "image_url": "/static/images/hotel-luxury-1.jpg"
    },
    {
        "id": "htl_402",
        "name": "CitizenUrban Boutique Hotel",
        "city": "New York",
        "location": "Chelsea / Flatiron District",
        "category": "standard",
        "stars": 4,
        "price_per_night": 165.0,
        "rating": 4.6,
        "reviews_count": 890,
        "badge": "Popular Choice",
        "amenities": ["Free Breakfast", "Workspace Pods", "Cocktail Bar", "Free WiFi"],
        "image_url": "/static/images/hotel-standard-1.jpg"
    },
    {
        "id": "htl_403",
        "name": "MetroPod Smart Budget Stay",
        "city": "New York",
        "location": "Queens Plaza, 10 min to Times Square",
        "category": "budget",
        "stars": 3,
        "price_per_night": 79.0,
        "rating": 4.3,
        "reviews_count": 640,
        "badge": "Best Value",
        "amenities": ["Free Ultra WiFi", "24/7 Front Desk", "Coffee Bar", "Luggage Storage"],
        "image_url": "/static/images/hotel-budget-1.jpg"
    },
    {
        "id": "htl_404",
        "name": "Pacific Bayfront Luxury Resort",
        "city": "San Francisco",
        "location": "Embarcadero Waterfront",
        "category": "luxury",
        "stars": 5,
        "price_per_night": 420.0,
        "rating": 4.9,
        "reviews_count": 980,
        "badge": "Waterfront Luxury",
        "amenities": ["Bay Views", "Infinity Pool", "Oyster & Wine Bar", "Spa", "Airport Chauffeur"],
        "image_url": "/static/images/hotel-luxury-2.jpg"
    },
    {
        "id": "htl_405",
        "name": "Sunset Gateway Inn",
        "city": "San Francisco",
        "location": "Sunset District, near Ocean Beach",
        "category": "budget",
        "stars": 3,
        "price_per_night": 88.0,
        "rating": 4.2,
        "reviews_count": 410,
        "badge": "Cozy & Affordable",
        "amenities": ["Free Parking", "Free Continental Breakfast", "WiFi"],
        "image_url": "/static/images/hotel-budget-2.jpg"
    },
    {
        "id": "htl_406",
        "name": "The Royal Palms Beach Hotel",
        "city": "Miami",
        "location": "South Beach Ocean Drive",
        "category": "luxury",
        "stars": 5,
        "price_per_night": 350.0,
        "rating": 4.8,
        "reviews_count": 1250,
        "badge": "Beachfront Luxury",
        "amenities": ["Private Beach", "Cabana Club", "Nightclub", "Spa & Wellness", "Free WiFi"],
        "image_url": "/static/images/hotel-luxury-3.jpg"
    },
    {
        "id": "htl_407",
        "name": "Biscayne Bay Breeze Inn",
        "city": "Miami",
        "location": "Downtown Miami",
        "category": "budget",
        "stars": 3,
        "price_per_night": 69.0,
        "rating": 4.1,
        "reviews_count": 520,
        "badge": "Budget Saver",
        "amenities": ["Outdoor Pool", "Free WiFi", "Breakfast Included"],
        "image_url": "/static/images/hotel-budget-3.jpg"
    }
]

POPULAR_DESTINATIONS = [
    {
        "name": "New York City",
        "country": "United States",
        "tagline": "The City That Never Sleeps",
        "starting_price": 45,
        "badge": "Most Popular",
        "services": ["Buses", "Trains", "Flights", "Hotels"],
        "gradient": "linear-gradient(135deg, #0052d4, #4364f7, #6fb1fc)"
    },
    {
        "name": "San Francisco",
        "country": "United States",
        "tagline": "Golden Gate & Coastal Charms",
        "starting_price": 58,
        "badge": "Trending",
        "services": ["Buses", "Trains", "Flights", "Hotels"],
        "gradient": "linear-gradient(135deg, #0f2027, #203a43, #2c5364)"
    },
    {
        "name": "Miami Beach",
        "country": "United States",
        "tagline": "Tropical Sun & Vibrant Nights",
        "starting_price": 69,
        "badge": "Hot Summer",
        "services": ["Flights", "Hotels"],
        "gradient": "linear-gradient(135deg, #ff7e5f, #feb47b)"
    },
    {
        "name": "Tokyo",
        "country": "Japan",
        "tagline": "Futuristic Skylines & Ancient Traditions",
        "starting_price": 890,
        "badge": "International",
        "services": ["Flights", "Hotels"],
        "gradient": "linear-gradient(135deg, #3a1c71, #d76d77, #ffaf7b)"
    },
    {
        "name": "Boston",
        "country": "United States",
        "tagline": "Historic Freedom Trail & Harbour Views",
        "starting_price": 45,
        "badge": "Weekend Getaway",
        "services": ["Buses", "Trains", "Hotels"],
        "gradient": "linear-gradient(135deg, #134e5e, #71b280)"
    },
    {
        "name": "Chicago",
        "country": "United States",
        "tagline": "World-Class Architecture & Deep Dish",
        "starting_price": 32,
        "badge": "Great Lakes",
        "services": ["Buses", "Trains", "Flights", "Hotels"],
        "gradient": "linear-gradient(135deg, #1f4037, #99f2c8)"
    }
]


class BookingService:
    """Core Search and Booking Operations Service."""

    @staticmethod
    def get_destinations():
        return POPULAR_DESTINATIONS

    @staticmethod
    def search_buses(origin, destination, travel_date=None):
        results = []
        origin_q = (origin or "").strip().lower()
        dest_q = (destination or "").strip().lower()

        for bus in BUS_INVENTORY:
            match_orig = not origin_q or origin_q in bus["origin"].lower()
            match_dest = not dest_q or dest_q in bus["destination"].lower()
            if match_orig and match_dest:
                results.append(bus)

        # If no strict match found, return all available buses so user always sees routes!
        return results if results else BUS_INVENTORY

    @staticmethod
    def get_bus_by_id(bus_id):
        for bus in BUS_INVENTORY:
            if bus["id"] == bus_id:
                return bus
        return None

    @staticmethod
    def search_trains(origin, destination, travel_date=None, train_class=None):
        results = []
        origin_q = (origin or "").strip().lower()
        dest_q = (destination or "").strip().lower()

        for train in TRAIN_INVENTORY:
            match_orig = not origin_q or origin_q in train["origin"].lower()
            match_dest = not dest_q or dest_q in train["destination"].lower()
            if match_orig and match_dest:
                results.append(train)

        return results if results else TRAIN_INVENTORY

    @staticmethod
    def get_train_by_id(train_id):
        for train in TRAIN_INVENTORY:
            if train["id"] == train_id:
                return train
        return None

    @staticmethod
    def search_flights(origin, destination, travel_date=None):
        results = []
        origin_q = (origin or "").strip().lower()
        dest_q = (destination or "").strip().lower()

        for flight in FLIGHT_INVENTORY:
            match_orig = not origin_q or origin_q in flight["origin"].lower() or origin_q in flight["origin_code"].lower()
            match_dest = not dest_q or dest_q in flight["destination"].lower() or dest_q in flight["destination_code"].lower()
            if match_orig and match_dest:
                results.append(flight)

        return results if results else FLIGHT_INVENTORY

    @staticmethod
    def get_flight_by_id(flight_id):
        for flight in FLIGHT_INVENTORY:
            if flight["id"] == flight_id:
                return flight
        return None

    @staticmethod
    def search_hotels(city=None, category=None, max_price=None):
        """
        Search hotels with budget vs luxury filtering:
        - category: 'all', 'budget', 'luxury', 'standard'
        """
        results = []
        city_q = (city or "").strip().lower()
        cat_q = (category or "all").strip().lower()

        for hotel in HOTEL_INVENTORY:
            match_city = not city_q or city_q in hotel["city"].lower() or city_q in hotel["location"].lower()
            match_cat = True

            if cat_q == "budget":
                match_cat = hotel["category"] == "budget" or hotel["price_per_night"] < 100.0
            elif cat_q == "luxury":
                match_cat = hotel["category"] == "luxury" or hotel["price_per_night"] >= 250.0
            elif cat_q == "standard":
                match_cat = hotel["category"] == "standard"

            if match_city and match_cat:
                results.append(hotel)

        return results if results else HOTEL_INVENTORY

    @staticmethod
    def get_hotel_by_id(hotel_id):
        for hotel in HOTEL_INVENTORY:
            if hotel["id"] == hotel_id:
                return hotel
        return None

    @staticmethod
    def create_booking(user_id, user_email, service_type, item_id, item_title, 
                       travel_date, passenger_name, passenger_phone="", 
                       seats=None, nights=1, total_amount=0.0, special_requests=""):
        """
        Creates and stores booking in database, sends AWS SNS confirmation.
        """
        prefix_map = {
            "bus": "BK-BUS",
            "train": "BK-TRN",
            "flight": "BK-FLT",
            "hotel": "BK-HTL"
        }
        prefix = prefix_map.get(service_type.lower(), "BK-GEN")
        unique_token = uuid.uuid4().hex[:8].upper()
        booking_id = f"{prefix}-{unique_token}"

        booking_data = {
            "booking_id": booking_id,
            "user_id": user_id,
            "user_email": user_email.strip().lower(),
            "service_type": service_type.lower(),
            "item_id": item_id,
            "item_title": item_title,
            "travel_date": travel_date or str(date.today() + timedelta(days=7)),
            "passenger_name": passenger_name,
            "passenger_phone": passenger_phone,
            "seats": seats or [],
            "nights": int(nights) if service_type.lower() == "hotel" else 1,
            "total_amount": float(total_amount),
            "special_requests": special_requests,
            "status": "CONFIRMED"
        }

        # Save to database
        saved = db.create_booking(booking_data)

        # Dispatch AWS SNS notification
        try:
            notification_service.send_booking_confirmation(saved, user_email)
        except Exception as e:
            # Booking still succeeds even if SNS temporarily fails
            pass

        return saved

    @staticmethod
    def cancel_booking(booking_id, user_id, user_email=None):
        """
        Cancels a booking and dispatches AWS SNS cancellation notice.
        """
        success, result = db.cancel_booking(booking_id, user_id)
        if success:
            recipient = user_email or result.get("user_email")
            try:
                notification_service.send_cancellation_confirmation(result, recipient)
            except Exception:
                pass
        return success, result


booking_service = BookingService()
