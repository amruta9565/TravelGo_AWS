# ✈️ TravelGo - Full-Stack AWS Cloud Travel Booking Platform

TravelGo is a full-stack, enterprise-grade cloud travel booking platform built with **Python Flask, Vanilla JavaScript, HTML5, CSS3, and AWS Services (DynamoDB, SNS, EC2, CloudWatch, Boto3)**.

---

## 🌟 Key Features

1. **User Authentication & Session Management**:
   - Secure registration and login with salted password hashing (`werkzeug.security`).
   - Session-based CSRF protection and HTTP-only cookies.
   - 1-Click Demo user login for fast local evaluation.
2. **Multi-Modal Travel Search & Booking**:
   - 🚌 **Buses**: Interactive, real-time visual coach seat selector (2+2 layout, 40 seats) with live pricing.
   - 🚆 **Trains**: Route selection, class tiers (Coach, Business, First), and amenities.
   - ✈️ **Flights**: Direct/stopover flight comparisons and fares.
   - 🏨 **Hotels**: Budget (< $100/night) and 5-Star Luxury resort filter tiers.
3. **Automated Cloud Notifications**:
   - Real-time booking confirmations and cancellation alerts dispatched via **AWS SNS** topics.
   - Built-in local mock logger when running offline without AWS credentials.
4. **User Dashboard & History**:
   - Profile management and key travel metrics (Total Spend, Active Trips).
   - Dynamic separation of **Upcoming Bookings** and **Past Travel History**.
   - Instant booking cancellation with refund tracking.
5. **Modern Blue & White Aesthetics**:
   - Modern responsive layout across desktops, tablets, and smartphones.

---

## 📁 Project Folder Structure

```
TravelGo_AWS/
├── .env.example              # Sample configuration with AWS toggles
├── .gitignore                # Git ignore rules (protects credentials and virtual environments)
├── README.md                 # Complete documentation
├── requirements.txt          # Python dependencies
├── run.py                    # Application launch entrypoint
├── config.py                 # Environment configurations (Dev, Prod, Test)
│
├── app/
│   ├── __init__.py           # Flask Application Factory & CSRF protection
│   ├── routes/
│   │   ├── main_routes.py    # Homepage, destinations, architecture overview
│   │   ├── auth_routes.py    # Login, registration, demo login, logout
│   │   ├── booking_routes.py # Bus seats, search, checkout, confirmation, cancellation
│   │   ├── dashboard_routes.py # User profile, upcoming/past booking views
│   │   └── api_routes.py     # JSON REST API for vanilla JS client interactivity
│   │
│   ├── services/
│   │   ├── db_service.py     # DynamoDB client with local mock JSON fallback
│   │   ├── auth_service.py   # Salted hashing and credentials validation
│   │   ├── booking_service.py# Inventory catalog and search engine
│   │   └── notification_service.py # AWS SNS email notifier with mock logger
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css      # Blue & white palette, buttons, badges, toasts
│   │   │   ├── navbar.css    # Responsive navigation bar & mobile drawer
│   │   │   ├── hero-search.css # Multi-modal search widget (Bus, Train, Flight, Hotel)
│   │   │   ├── cards.css     # Destination cards & AWS feature highlights
│   │   │   ├── booking.css   # Results layout & dynamic bus seat selection
│   │   │   ├── dashboard.css # Profile header, stats cards, cancellation modal
│   │   │   └── auth.css      # Login and registration card styling
│   │   └── js/
│   │       ├── api.js        # Fetch helper with CSRF header injection
│   │       ├── search.js     # Search tabs and hotel category filters
│   │       ├── seat-selection.js # Interactive seat grid and price calculator
│   │       ├── dashboard.js  # Tabs switcher and cancellation modal triggers
│   │       └── main.js       # Mobile menu, toasts, and alert dismissals
│   │
│   └── templates/
│       ├── base.html         # Master template layout with header & footer
│       ├── index.html        # Landing page with hero and destination cards
│       ├── search_results.html # Search results with filter sidebar
│       ├── bus_seats.html    # Interactive bus seat selection floor plan
│       ├── booking_confirm.html # Checkout form and printable voucher
│       ├── dashboard.html    # Profile, upcoming trips & past booking history
│       ├── login.html        # Login page with demo button
│       ├── register.html     # Registration form
│       ├── about.html        # AWS Cloud architecture explanation
│       └── errors/           # Custom 404 and 500 error pages
│
├── aws/                      # AWS Setup scripts & deployment resources
│   ├── dynamodb_setup.py     # Provisions DynamoDB tables and GSIs
│   ├── sns_setup.py          # Provisions SNS Topic and subscriptions
│   ├── iam_policy.json       # Least-privilege IAM policy document
│   └── ec2_user_data.sh      # EC2 launch bootstrap script
│
└── tests/                    # Automated Pytest Suite (21 Passing Tests)
    ├── conftest.py           # Test fixtures and mock state reset
    ├── test_auth.py          # Registration, login, validation tests
    ├── test_search.py        # Multi-modal search and hotel filter tests
    ├── test_booking.py       # Seat selection and booking creation tests
    ├── test_cancellation.py  # Cancellation flow and SNS alert tests
    └── test_dashboard.py     # Dashboard stats and upcoming/past tests
```

---

## 🚀 How to Run Locally (Step-by-Step for Beginners)

### 1. Prerequisites
Ensure you have **Python 3.10+** and **Git** installed on your computer.

### 2. Set Up Virtual Environment
In your terminal (Command Prompt or PowerShell):
```powershell
cd c:\TravelGo_AWS
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Create Environment File
Copy the provided example file:
```powershell
copy .env.example .env
```
*(By default, `USE_MOCK_AWS=true` is enabled, which means you can immediately test all features without needing an AWS account or incurring any charges!)*

### 5. Start the Application
```powershell
python run.py
```
Open your web browser and navigate to:
👉 **`http://127.0.0.1:5000`**

### 6. Quick Demo Login
On the homepage or sign-in page, click **"⚡ Demo User"** or **"⚡ 1-Click Demo Login"** to instantly test the platform with a pre-configured account (**Alex Traveler**).

---

## 🧪 Running Automated Tests

Run the comprehensive Pytest suite:
```powershell
.\venv\Scripts\pytest -v
```
All 21 tests will run and verify:
- ✅ User registration, password hashing, and authentication
- ✅ Multi-modal search (Bus, Train, Flight)
- ✅ Budget (< $100) and Luxury (5-Star) hotel filters
- ✅ Dynamic bus seat selection and fare recalculation
- ✅ Booking creation and AWS SNS email dispatch
- ✅ Booking cancellation and refund processing
- ✅ User dashboard, upcoming bookings, and past history views

---

## ☁️ AWS Cloud Production Deployment

When ready to deploy on **Amazon Web Services**:
1. **DynamoDB Tables**:
   ```bash
   python aws/dynamodb_setup.py
   ```
2. **SNS Notifications Topic**:
   ```bash
   python aws/sns_setup.py your-email@example.com
   ```
3. **EC2 Deployment**:
   - Launch an EC2 instance (Amazon Linux 2023 or Ubuntu 22.04).
   - Attach an IAM Role with the permissions specified in [`aws/iam_policy.json`](aws/iam_policy.json).
   - Provide [`aws/ec2_user_data.sh`](aws/ec2_user_data.sh) as the instance launch User Data.
