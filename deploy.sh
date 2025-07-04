#!/bin/bash

# Logging setup (optional)
exec > >(tee /var/log/deploy.log | logger -t deploy -s 2>/dev/console) 2>&1

# Variables
APP_USER=ec2-user
APP_HOME=/home/$APP_USER
APP_DIR=$APP_HOME/my_weather

# --- 1. Update system and install system packages ---
sudo yum update -y
sudo yum install -y git nginx

# Enable Python 3.8 and install it
sudo amazon-linux-extras enable python3.8
sudo yum install -y python3.8 python3.8-devel

# Install pip manually (Amazon Linux 2 doesn't include it for 3.8)
cd /tmp
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3.8 get-pip.py

# Set Python 3.8 and pip as system defaults
sudo alternatives --install /usr/bin/python python /usr/bin/python3.8 1
sudo alternatives --install /usr/bin/pip pip /usr/local/bin/pip3.8 1

# Install virtualenv
sudo pip install virtualenv

# --- 2. Clone and set up FastAPI project as ec2-user ---
sudo -u $APP_USER bash <<EOF
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn uvicorn
EOF

# --- 3. Set up Gunicorn systemd service ---
sudo tee /etc/systemd/system/myweather.service > /dev/null <<EOF
[Unit]
Description=MyWeather FastAPI App
After=network.target

[Service]
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable myweather
sudo systemctl start myweather

# --- 4. Configure NGINX reverse proxy ---
sudo tee /etc/nginx/conf.d/myweather.conf > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

sudo systemctl enable nginx
sudo systemctl restart nginx
