#!/bin/bash

# Logging
exec > >(tee /var/log/user-data.log | logger -t user-data -s 2>/dev/console) 2>&1

# --- 1. Update System and Install Required Packages ---
yum update -y

# Enable Python 3.8
amazon-linux-extras enable python3.8
yum install -y python3.8 python3.8-devel git nginx

# Create symlinks
alternatives --install /usr/bin/python python /usr/bin/python3.8 1
alternatives --install /usr/bin/pip pip /usr/bin/pip3.8 1

# Install pip + virtualenv
pip install --upgrade pip
pip install virtualenv

# --- 2. Clone FastAPI Repo ---
#cd /home/ec2-user
#git clone https://github.com/duncannevin/my_weather.git
#cd my_weather

# Create virtual environment and install dependencies
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn uvicorn

# --- 3. Create systemd Service for Gunicorn + Uvicorn ---
cat <<EOF > /etc/systemd/system/myweather.service
[Unit]
Description=MyWeather FastAPI App
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/my_weather
Environment="PATH=/home/ec2-user/my_weather/venv/bin"
ExecStart=/home/ec2-user/my_weather/venv/bin/gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000

Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable myweather
systemctl start myweather

# --- 4. Configure NGINX as a Reverse Proxy on Port 80 ---
cat <<EOF > /etc/nginx/conf.d/myweather.conf
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

# Enable and start NGINX
systemctl enable nginx
systemctl restart nginx
