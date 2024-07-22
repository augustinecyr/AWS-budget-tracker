# Commands & Configurations

## Connecting to AWS RDS database via CLI

`mysql -h <rds-endpoint> -u admin -p`

## flaskapp.service

```
[Unit]
Description=Flask Application
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/budget_tracker
ExecStart=/usr/bin/python3 /home/ec2-user/budget_tracker/app.py

[Install]
WantedBy=multi-user.target
```

### flaskapp.service commands

```
sudo nano /etc/systemd/system/flaskapp.service
sudo systemctl daemon-reload
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
sudo systemctl status flaskapp
sudo nano /etc/httpd/conf.d/flaskapp.conf
```

## Request forwarding for Apache as Reverse Proxy

```
<VirtualHost \*:80>
ServerName your_ec2_instance_ip
ProxyRequests Off
ProxyPreserveHost On
ProxyPass / http://127.0.0.1:8080/
ProxyPassReverse / http://127.0.0.1:8080/
</VirtualHost>
```

## Standard Commands

```
sudo systemctl start httpd
sudo systemctl enable httpd
sudo systemctl restart httpd
sudo yum update -y
sudo yum groupinstall "Development Tools" -y
sudo yum install python3 python3-pip python3-devel -y
sudo pip3 install --upgrade pip
sudo pip3 install flask pymysql
```

## SQL CLI Commands

```
USE budget_tracker;

SHOW TABLES;

DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS income;

CREATE TABLE expenses (
id INT AUTO_INCREMENT PRIMARY KEY,
amount DECIMAL(10, 2) NOT NULL,
category VARCHAR(255) NOT NULL,
date DATE NOT NULL,
description TEXT
);

CREATE TABLE income (
id INT AUTO_INCREMENT PRIMARY KEY,
amount DECIMAL(10, 2) NOT NULL,
source VARCHAR(255) NOT NULL,
date DATE NOT NULL,
description TEXT
);
```
