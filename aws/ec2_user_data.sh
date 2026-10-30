#!/bin/bash
# ========================================================
# TravelGo EC2 User Data Bootstrap Script (Amazon Linux 2023 / RHEL)
# Automatically provisions runtime, virtual environment, and systemd service.
# ========================================================

set -e
echo "Starting TravelGo EC2 Provisioning..."

# 1. Update OS packages
dnf update -y
dnf install -y python3-pip python3-devel git gcc

# 2. Setup application directory
APP_DIR="/opt/travelgo"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# 3. Clone or pull repository (Replace with your GitHub repo URL)
# git clone https://github.com/your-username/travelgo.git .

# 4. Create isolated Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# 5. Create production environment file using EC2 instance role
cat <<EOF > .env
FLASK_APP=run.py
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=$(openssl rand -hex 32)
PORT=5000
USE_MOCK_AWS=false
AWS_REGION=us-east-1
DYNAMODB_USERS_TABLE=travelgo_users
DYNAMODB_BOOKINGS_TABLE=travelgo_bookings
SNS_BOOKING_TOPIC_ARN=arn:aws:sns:us-east-1:$(aws sts get-caller-identity --query Account --output text):travelgo-booking-alerts
EOF

# 6. Configure systemd service
cat <<EOF > /etc/systemd/system/travelgo.service
[Unit]
Description=TravelGo AWS Cloud Booking Platform
After=network.target

[Service]
User=ec2-user
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 run:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 7. Start and enable service
systemctl daemon-reload
systemctl enable travelgo
systemctl start travelgo

echo "TravelGo EC2 deployment completed successfully on port 5000!"
