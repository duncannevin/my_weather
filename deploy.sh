#!/bin/bash

# Detect and set user home directory
APP_USER=ec2-user
APP_DIR=/home/$APP_USER/my_weather

# Run everything as root except application install
yum update -y
yum install -y git nginx
amazon-linux-extras enable python3.8
yum install -y python3.8 python3.8-devel

alternatives --install /usr/bin/python python /usr/bin/python3.8 1
alternatives --install /usr/bin/pip pip /usr/bin/pip3.8 1

pip install --upgrade pip
pip install virtualenv

# Switch to ec2-user for app install
sudo -u $APP_USER bash <<EOF
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn uvicorn
EOF

# Create systemd service (as root)
cat <<EOF > /etc/systemd/system/myweather.service
[Unit]
Description=MyWeather FastAPI App
After=network.target

[Service]
User=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable myweather
systemctl start myweather

# Configure NGINX
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

systemctl enable nginx
systemctl restart nginx
