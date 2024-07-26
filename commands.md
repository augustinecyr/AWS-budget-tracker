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

CREATE TABLE `expenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `month` varchar(50) NOT NULL,
  `money_in` decimal(10,2) NOT NULL,
  `money_out` decimal(10,2) NOT NULL,
  `total` decimal(10,2) GENERATED ALWAYS AS ((`money_in` - `money_out`)) STORED,
  PRIMARY KEY (`id`),
  KEY `username` (`username`),
  CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`username`) REFERENCES `users` (`username`)
) 

CREATE TABLE `users` (
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`username`)
) 
```
