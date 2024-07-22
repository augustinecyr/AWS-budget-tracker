# User Data Start-up script for EC2 Instance
```
#!/bin/bash
```
## Update package repositories and install necessary packages
```
sudo yum update -y
sudo yum install httpd php php-cli php-pdo php-fpm php-json php-mysqlnd python3 python3-pip -y
```
## Install MySQL client
```
sudo wget https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm
sudo dnf install mysql80-community-release-el9-1.noarch.rpm -y
sudo rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2023
sudo dnf install mysql-community-client -y
```
## Start and enable Apache web server
```
sudo systemctl start httpd
sudo systemctl enable httpd
```
## Display server status
```
sudo systemctl status httpd
```