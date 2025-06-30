# 🍽️ Halal Palace – Smart Restaurant Management System

A comprehensive Python + MySQL-based application that lets customers book tables, order food, and pay via UPI or cash, with built-in login/register system, password recovery, and an admin dashboard for managing bookings and orders.

> This project showcases end-to-end restaurant automation.
---

# Features

# Customer
- Register and Login
- Forgot Password Recovery
- Book Table (₹50 booking fee)
- Choose Payment Method: Cash or UPI
- Food Ordering from Menu
- Payment Status Handling (Pending/Paid)

# Admin
- Secure Admin Login
- View All Reservations
- View All Orders
- Filter by Payment Status
- Track Customer Booking & Orders


# Tech Stack
- Python 3.x
- MySQL (Backend Database)
- `mysql-connector-python` (DB Connectivity)


# Technologies used
Python, MySQL, Pandas, QR Code, File Handling, Error Handling, Regex, Modular Programming, CRUD Operations, Authentication.

# 📌 Future Enhancements
-GUI using Tkinter or Web App using Django
-Real-time UPI Payment Verification with Razorpay API
-Email/SMS confirmations
-Order history and receipts
-Admin analytics dashboard

# Database setup
# Before running this project, ensure you have MySQL installed and running. You must manually create the following database and tables.
-CREATE DATABASE databasename,
-CREATE TABLE customers(user_name,password,full_name,gender,phone_number,email_id)
-CREATE TABLE admin(admin_id,password)
-CREATE TABLE menu_items(order_id,name,category,price,stock_quantity)
-CREATE TABLE orders(order_id,customer_name,total_price,payment_method,order_time,payment_status,payment_note,payment_attempts)
-CREATE TABLE order_items(order_item_id,order_id,item_name,price,quantity)
-CREATE TABLE tables(table_number)
-CREATE TABLE reservations(reservation_id,customer_name,table_number,booking_date,booking_fee_payment,created_at,booking_duration)

# 🙋‍♂️ Author
Kacheri Thahir
MCA Graduate | Aspiring Software Engineer
Linkedin:www.linkedin.com/in/
kacheri-thahir-307b61309

