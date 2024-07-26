# Budget Tracker Application with AWS Academy Lab

## Overview

This project sets up a Budget Tracker application on an AWS EC2 instance using a custom VPC, Elastic IP, and Apache as a reverse proxy. The backend is developed with Flask, and the frontend uses HTML and Bootstrap for user interaction. The application interacts with a MySQL RDS database for data storage and management.

## Setup Steps

1. **Create EC2 Instance:**

   - Set up a VPC with necessary subnets.
   - Enable ports for database access.
   - Create security groups to control access.
   - Assign an Elastic IP for a fixed IP address.

2. **Install Necessary Packages:**

   - Install Python, Apache, MySQL client, and other dependencies.
   - Check Apache installation by verifying the default page.

3. **Automatic Configuration:**

   - Write user data scripts for automatic configuration during instance boot.

4. **Application Setup:**

   - Develop the backend with `app.py` using Python and Flask.
   - Create HTML templates for the frontend.
   - Set up directories on the EC2 instance to store application files.

5. **Apache Configuration:**

   - Change Apache's default configuration to route the homepage to `login.html` using Flask.
   - Create a systemd service file (`flaskapp.service`) to ensure `app.py` runs on boot.

6. **Database Setup:**
   - Link MySQL RDS to the EC2 instance securely.
   - Create and configure the database and tables (`expenses`, `income`).

## Features Implemented

- Basic HTML and Flask application for adding expenses.
- Expense editing functionality.
- Secure communication between the app and the MySQL database.
- Integrate Bootstrap for a better UI.
- Added forecasting feature to predict future expenses.

## Future Enhancements

- Add more features for admin use case.
- Explore pulling records from RDS using S3 Bucket.
- Explore storing app.log file into S3 Bucket.

---
