# -------------------------------------login section--------------------------------------------------

import mysql.connector
import re
import sys
import os

conn = mysql.connector.connect(
    host="your_host_name",
    user="your_user_name",                    # db username
    password="your_password",         # db password
    database="database name "      # db name
)

cursor = conn.cursor()


def register(cursor,conn):
    print("\n WELCOME TO HALAL PALACE REGISTRATION" )
    while True:
        user_name=input("Choose a user_name: ").strip().lower()
        cursor.execute("SELECT * FROM customers WHERE user_name=%s",(user_name,))
        if cursor.fetchone():
            print("Username already exists, please login.")
            sys.exit()
        else:
            break

    full_name=input("Enter Full Name:")
    gender=input("Enter your gender (Male/Female):").lower()
    phone_number=input("Enter your Phone number:")
    email_id=input("Enter your Email:")
    
    while True:
        password=input("Choose a password(Combination of \" Capital letter, Numbers and a Special Character\"):").strip()
        if (len(password) < 7 or
        not re.search(r"[A-Z]",password) or
        not re.search(r"[0-9]",password) or
        not re.search(r"[\W_]",password)):
            print("Weak Password. Try again.")
        else:
            break

    insert_query=("""
        INSERT INTO customers(user_name,password,full_name,gender,phone_number,email_id)
        VALUES (%s,%s,%s,%s,%s,%s)""")
    cursor.execute(insert_query,(user_name,password,full_name,gender,phone_number,email_id))
    conn.commit()
    print(f"Registered SUccessfully!\nWelcome,{full_name}")
    return user_name


#--------------------------------------------------------------------

def login(cursor,conn):
    print("\n WELCOME TO HALAL PALACE LOGIN ")
    user_name=input("Enter your username:")
    password=input("Enter your password:")

    cursor.execute("SELECT full_name FROM customers WHERE user_name=%s AND password=%s",(user_name,password))
    result=cursor.fetchone()
    if result:
        full_name=result[0]
        print(f"Welcome Back, {full_name}!")
        with open("session_user.txt","w") as f:
            f.write(full_name)
        return full_name
    else:
        print("Incorrect username or password.")
        return None
    
#----------------------------------------------------------------------------------

def forgot_password(cursor,conn):
    print("\n FORGOT PASSWORD")
    username=input("Enter your username:")
    phonenumber=input("Enter your phone number:")
    cursor.execute("SELECT * FROM customers WHERE user_name=%s AND phone_number=%s",(username,phonenumber))
    user=cursor.fetchone()
    if user:
        while True:
            new_password=input("Enter your new password (Combination of \" Capital letter, Numbers and a Special Character\"):").strip()
            if (len(new_password) < 7 or
            not re.search(r"[A-Z]",new_password) or
            not re.search(r"[0-9]",new_password) or
            not re.search(r"[\W_]",new_password)):
                print("Weak Password. Try again.")
            else:
                break
        cursor.execute("UPDATE customers SET password=%s WHERE user_name=%s ",(new_password,username))
        conn.commit()
        print("Password Updated Successfully")
    else:
        print("No User Found..")


#----------------------------------------------------------------------------

def logout():
    if os.path.exists("session_user.txt"):
        os.remove("session_user.txt")
        print("You have been logged out!")
    else:
        print("You are not logged in.")



#------------------------------------------------------------------------------------------


def combined_login(cursor,conn):
    # Checking for existing login 
    if os.path.exists("session_user.txt"):
        with open("session_user.txt","r") as f:
            user_name=f.read().strip()
            if user_name:
                print(f"Welcome Back {user_name}!")
                return user_name
    
    while True:
        print("\n Welcome, Choose your Login Method:\n1. Register\n2. Login\n3.Forgot Password")
        choice=input("Enter your Login Method type (1/2/3):").strip()
        if choice=="1":
            user=register(cursor,conn)
            if user:
                with open("session_user.txt","w")  as f:
                    f.write(user)
                return user
            
        elif choice=="2":
            user=login(cursor,conn)
            if user:
                with open("session_user.txt","w")  as f:
                    f.write(user)
                return user
            else:
                print("Please register first.")
                sys.exit()

        elif choice=="3":
            forgot_password(cursor,conn)
            sys.exit()
        else:
            print("Invalid choice,please try again.")
            

