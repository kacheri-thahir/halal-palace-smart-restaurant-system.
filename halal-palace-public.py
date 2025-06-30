import sys
import time
import qrcode
import gender_guesser.detector as gender
import mysql.connector
from datetime import datetime as dt,timedelta
from Halal_palace_login_public import combined_login 


# Establish connection
conn = mysql.connector.connect(
    host="your_host_name",
    user="your_user_name",                    #  username
    password="your_password",         #  password
    database="database_name"      # db name
)

cursor = conn.cursor()


def spinning_dance_text(text, repeat=10, delay=0.2):
    spinner = ['❤️', '🍗', '😋', '🍴'] 
    width = 100

    for i in range(repeat):
        spin = spinner[i % len(spinner)]
        offset = (i % 10) * 2  
        print(" " * offset + spin + " " + text + " " + spin, end='\r', flush=True)
        time.sleep(delay)
    
    print(text.center(width))  

# print("\n" + "*" * 100)
spinning_dance_text("WELCOME")
spinning_dance_text("TO")
spinning_dance_text("\"HALAL PALACE\"")
# print("*" * 100)



user_name=combined_login(cursor,conn)               #connection of login,register & forgot password
if not user_name:
    print("Exiting....")
    sys.exit()


d=gender.Detector()         #Creating gender detector object
gussed_gender=d.get_gender(user_name)

#Deciding gender based on name:
if gussed_gender=="male":
    title="Sir"
elif gussed_gender=="female":
    title="Ma'am"
else:
     title="Guest"

print(f"Welcome {title} {user_name}!We're happy to have you at Halal Palace.")

# ----------------------------------------------------------------------------------------------(Table booking section)

book=input(f"Do you want to Book your table {user_name},{title} (yes/No):")       #table booking information
if book=="yes":
        booking_date=input("Enter Booking Date (YYYY-MM-DD):").strip()
        booking_time=input("Enter Booking Time (HH:MM (24-HOUR FORMAT)):").strip()
        booking_duration= int(input("How long do you want to stay (in minutes(E.g: 1Hr-60)): "))

        # Convert entered booking time for calculations

        new_start = dt.strptime(booking_time,"%H:%M")
        new_end = new_start + timedelta(minutes=booking_duration)

        #  Find all unavailable seat numbers at that date/time
        cursor.execute("""
            SELECT table_number,booking_time,booking_duration FROM reservations WHERE booking_date=%s""",(booking_date,))
        bookings=cursor.fetchall()      #booked tables will be stored here

        booked_tables=set()                                                 #This whole code check time conflicts between booking tables 
        for table,existing_time,dur in bookings:
            existing_start=dt.strptime(str(existing_time),"%H:%M:%S")
            existing_end = existing_start + timedelta(minutes=dur)
            if new_start < existing_end and new_end > existing_start:
                booked_tables.add(table)                                       #till this code
                print(f"Table is already booked from {existing_start.strftime('%H:%M')} to {existing_end.strftime('%H:%M')}")

        # Get all tables
        cursor.execute("SELECT table_number from tables")
        all_tables=[t[0] for t in cursor.fetchall()]

        # filter available seats
        available_tables=[t for t in all_tables if t not in booked_tables]
        if not available_tables:
            print("Sorry! This Table is booked for this time.You can book another table.")
        else:
            print("Available Tables:",available_tables)
            table_number=int(input("Select your preferred table number:"))
            if table_number not in available_tables:
                print("This table is booked.You can try another table.")
                sys.exit()
            else:
                booking_fee=50          #table booking fee
                print("Table Booking fee is ₹.50, you must pay now to confirm.")

                booking_mode=input("Are you booking Online or at the Restaurant?(online/walk-in):").lower().strip()                     
                payment_method=input("Select your payment method \n CASH, PHONEPAY, GOOGLEPAY, PAYTM, OR any other UPI : ").lower().strip()
                if booking_mode=="online"and payment_method=="cash":                #adding condition for online booking and cash payment
                    print("Cash payment is not allowed for Online booking please select upi.")
                    sys.exit()

                booking_confirmed=False                 #Default booking confirmation is false
                if payment_method=="cash":
                    try:
                        booking_amount=float(input("Pay Rs.50 for booking:"))
                        if booking_amount==50:
                            booking_confirmed=True
                            print("Table Booked..")
                        else:
                            print("Payment not received, Booking Cancelled..")
                    except:
                        print("INVALID PAYMENT...")

                elif payment_method in ["phonepay","googlepay","paytm","upi"]:
                    upi_id="your_upi_id"
                    upi_url=f'upi://pay?pa={upi_id}&pn=REcipient%20Name'
                    qr=qrcode.make(upi_url)
                    qr.show()

                    paid=input("Please scan and type 'done' after payment:").lower()
                    if paid=="done":
                        booking_confirmed=True
                        print("payment completed..")
                    else:
                        print("payment not confirmed, Booking Cancelled...")
                else:
                    print("INVALID PAYMENT METHOD")

                if booking_confirmed:
                    insert_reservation="""
            INSERT INTO reservations(customer_name,table_number,booking_date,booking_time,booking_fee_payment)
            VALUES(%s,%s,%s,%s,TRUE)"""
                    
                    cursor.execute(insert_reservation,(user_name,table_number,booking_date,booking_time))
                    conn.commit()
                    print(f"Table {table_number} Booked sucessfully for {booking_date} at {booking_time}")
                    sys.exit()
                else:
                    print("Table not booked due to failed payment")
                    sys.exit()

else:
    print(f"😋 No Problem {title}, you can order food directly..")

    
#--------------------------------------------------------------------------------------------------------------(Food ordering section)

menu = {
    "NON-VEG-ITEMS": [
        {"name": "Nizami Chicken Biryani", "price": 280},
        {"name": "Royal Butter Chicken", "price": 260},
        {"name": "Shahi Mutton Rogan Josh", "price": 300},
        {"name": "Mughlai Chicken Korma", "price": 270},
        {"name": "Afghani Grilled Chicken", "price": 250},
        {"name": "Fish Tikka Masala", "price": 240},
        {"name": "Mutton Dum Biryani - Nawabi Style", "price": 290},
        {"name": "Chicken Changezi", "price": 260},
        {"name": "Royal Egg Curry Masala", "price": 180},
        {"name": "Tandoori Chicken Masala", "price": 250},
        {"name": "Hyderabadi Mutton Handi", "price": 310},
        {"name": "Prawn Curry Royale", "price": 320},
        {"name": "Mughlai Chicken Lababdar", "price": 275},
        {"name": "Lamb Nihari", "price": 330},
        {"name": "Royal Keema Mutter", "price": 290}
    ],
    "VEG-ITEMS": [
        {"name": "Shahi Paneer Nawabi", "price": 220},
        {"name": "Mughlai Vegetable Handi", "price": 200},
        {"name": "Royal Kofta Curry", "price": 210},
        {"name": "Nawabi Dal Makhani", "price": 180},
        {"name": "Veg Hyderabadi Biryani", "price": 190},
        {"name": "Subz Diwani Handi", "price": 200},
        {"name": "Paneer Lababdar Royale", "price": 215},
        {"name": "Angoori Aloo Curry", "price": 170},
        {"name": "Kashmiri Dum Aloo", "price": 185},
        {"name": "Rajasthani Gatta Curry", "price": 190}
    ],
    "STARTERS": [
        {"name": "Nawabi Paneer Tikka", "price": 150},
        {"name": "Shahi Veg Kebab Platter", "price": 160},
        {"name": "Royal Reshmi Seekh", "price": 180},
        {"name": "Mughlai Malai Broccoli", "price": 140},
        {"name": "Emperor's Chicken 65", "price": 160},
        {"name": "Hyderabadi Veg Lollipop", "price": 130},
        {"name": "Maharaja Fish Fingers", "price": 190},
        {"name": "Cheesy Mughlai Corn Balls", "price": 145},
        {"name": "Zafrani Chicken Tikka", "price": 175},
        {"name": "Nawabi Mushroom Delight", "price": 155},
        {"name": "Royal Chicken Wings", "price": 170},
        {"name": "Peshawari Veg Rolls", "price": 135},
        {"name": "Lamb Galouti Kebab", "price": 200},
        {"name": "Royal Masala Papad Tower", "price": 100},
        {"name": "Tandoori Stuffed Aloo", "price": 125},
        {"name": "Hariyali Paneer Kebabs", "price": 160},
        {"name": "Chicken Malai Shots", "price": 180},
        {"name": "Royal Prawns Tempura", "price": 210},
        {"name": "Dum Ke Chilli Babycorn", "price": 130},
        {"name": "Nawabi Egg Pakoda", "price": 110}
    ]
}


menu_replay=input(f"wanna See Menu, {user_name} {title} (yes/No):").lower()
while True:

    if menu_replay=='yes'.lower():
        
        max_length=max(len(menu["NON-VEG-ITEMS"]),len(menu["VEG-ITEMS"]),len(menu["STARTERS"]))
        print(f"\n{'🥩 NON-VEG-ITEMS':^31} {'🥗 VEG-ITEMS':^50} {' 🍗 STARTERS':^19} ")
        print('-'*122)

        for i in range(max_length):
                nonveg=f'{menu["NON-VEG-ITEMS"][i]["name"]}-₹{menu["NON-VEG-ITEMS"][i]["price"]}' if i<len(menu["NON-VEG-ITEMS"]) else ""
                veg=f'{menu["VEG-ITEMS"][i]["name"]}-₹{menu["VEG-ITEMS"][i]["price"]}' if i<len(menu["VEG-ITEMS"]) else ""
                starter=f'{menu["STARTERS"][i]["name"]}-₹{menu["STARTERS"][i]["price"]}' if i<len(menu["STARTERS"]) else ""
                print(f"{nonveg:<40}|{veg:<40}|{starter}") 
        break

    else:
        print("No problem, Sir. Have a great day!")
        sys.exit()

flat_menu = {}          #making all menu like non veg,veg,starters into one menu i.e., flat_menu
for category_items in menu.values():
    for item in category_items:
        flat_menu[item["name"].lower()] = item["price"]

order_total=0
order_summary=[] #Track items customer selected #list to store ordered items
while True:
        orders=input("Your fav item can Order here:  ").strip().lower()
        if orders in flat_menu:
            order_total+=flat_menu[orders] 
            order_summary.append(orders)
            print(f"Your item {orders.title()} has been added to your order")
        else:
            print(f"Sorry {title}, We Dont have this food item... ") 
            continue

        another_order = input("Do you want to add another item? (yes/no): ").strip().lower()
        if another_order.lower()!= 'yes':
            break


print(f"{user_name} {title}, Your Order will be ready in few minuates ... ")
time.sleep(3)

print("🍴Keep Enjoying 😋")
time.sleep(5)

 
print(f"Thank you..\n Here is your Bill {title}..")
print(f"💸The total amount to pay is Rs.{order_total} Only ")


payment=input("Payment Method: \n CASH, UPI :").lower()

payment_status='pending'        #defining status default pending
payment_note=''
payment_attempts=0

if payment == "CASH".lower():
    try:
        print("You selected cash payment.")                     
        print("please pay the bill at billing counter.")

            # Insert order into database
        insert_order = """
            INSERT INTO orders (customer_name, total_price, payment_method,payment_status)
            VALUES (%s, %s, %s,%s)
        """
        order_data = (user_name, order_total, payment,'pending')
        cursor.execute(insert_order, order_data)
        conn.commit()

        #  Get order ID of the last inserted order
        order_id = cursor.lastrowid

        print(f"Please tell this Order id:{order_id} at Billing counter to confirm payment.")

        #  Insert each item into order_items table
        for item_name in order_summary:  # This tracks each item selected
            price = flat_menu[item_name]
            insert_item = """
                INSERT INTO order_items (order_id, item_name, price, quantity)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_item, (order_id, item_name.title(), price, 1))  # Quantity = 1
            conn.commit()


    except ValueError:
        print("❌ Invalid payment. Please check again and pay.")


if payment== "UPI".lower():
    upi_id="your_upi_id"
    upi_url=f'upi://pay?pa={upi_id}&pn=REcipient%20Name'
    platform=input("Please Mention UPI PAYMENT platform:").lower().strip()
  

while True:
    qr=qrcode.make(upi_url)
    qr.show()
    payment_attempts=+1                 #here we are adding payment_attempts row to check how many times customer scaned upi scaner
    payment_input=input("Please Scan the QR and type 'done' Once you complete the payment or type 'cancel' to switch to cash: ").lower().strip()

    if payment_input=='done':           #if done then payment will be successfully completed no problem
        payment_status='paid'
        payment_note="paid via upi"
        print("✅ Payment is Successful.")
        print(f"💕Thankyou for visiting \"HALAL PALACE\"\n 🫰 Have a Great Day {title}..")
        break
    elif payment_input=='cancel':       #if customer type cancel payment_input switches to cash.
        payment='cash'                 
        payment_status='pending'            
        payment_note="UPI failed, Switched to cash"       
        print("UPI cancelled. Switching to cash payment.. ")
        break
    else:
        print("payment not yet completed.please scan and complete payment.")        

if payment == 'cash':                               #if customer switches to cash payment by typing cancel this will be displayed.
    print("💵 Please pay at the billing section.")
    payment_status = 'pending'
    payment_note = 'Selected cash at counter'

        #  Insert order into database
insert_order = """
    INSERT INTO orders (customer_name, total_price, payment_method,payment_status,payment_note,payment_attempts)
    VALUES (%s, %s, %s,%s,%s,%s)
"""
order_data = (user_name, order_total, platform,payment_status,payment_note,payment_attempts)
cursor.execute(insert_order, order_data)
conn.commit()

    #  Get order ID of the last inserted order
order_id = cursor.lastrowid

    #  Insert each item into order_items table
for item_name in order_summary:  # This tracks each item selected
    price = flat_menu[item_name]
    insert_item = """
        INSERT INTO order_items (order_id, item_name, price, quantity)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_item, (order_id, item_name.title(), price, 1))  # Quantity = 1
conn.commit()
print(f"🧾 Order ID {order_id} stored with status: {payment_status}")


logout_choice=input("Do you want to logout?(yes/No):").lower()
if logout_choice=="yes":
    from Halal_palace_login_public import logout
    logout()
    