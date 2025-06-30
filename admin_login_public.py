import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host="your_host_name",
    user="your_user_name",                    # db username
    password="your_password",         # db password
    database="database name "      # db name
)

cursor = conn.cursor()


print("WELCOME TO HALAL PALACE ADMIN MODE".center(100,'*'))

def admin_login():
    admin_id=input("Enter your id:")
    password=input("Enter your password:")

    # NOTE: For real applications, store hashed passwords and use secure comparison
    cursor.execute("SELECT * FROM admin WHERE admin_id=%s AND password=%s",(admin_id,password))
    result=cursor.fetchone()
    if result:
        print(f"Welcome back,{admin_id}!")
        return True
    else:
        print("Access denied!")
        return False
    
def admin_pannel():
    while True:
        print("\n")
        print("Admin panel options".center(100,'*'))
        print("\n")
        print(" 1.View all orders\n 2.View sales report\n 3.Update an order\n 4.Delete an order\n 5.View pending cash payments\n 6.Mark Cash payment as paid\n 7.Mark selected into cash payments are paid\n 8.Exit")
        option=int(input("Select a Option(1-8):"))
        if option==1:
            cursor.execute("SELECT * FROM orders")
            rows=cursor.fetchall()
            print("All Orders".center(100,'*'))
            print("\n")
            for row in rows:
                print(row)

        
        if option==2:
            order_df=pd.read_sql("SELECT * FROM orders",conn)
            item_df=pd.read_sql("SELECT * FROM order_items",conn)

            print(f"\n Total sales: ₹{order_df['total_price'].sum()}")
            top_items=item_df['item_name'].value_counts().head(5)
            print(f"🔥Top items-\n{top_items}")

        
        if option==3:
            order_id=input("Enter order id you want to update:")
            new_name=input("Enter New name you want to update:")
            new_price=input("Enter New price you want to update:")
            new_payment=input("Enter New payment you want to update:")
            update_query = """
                UPDATE orders
                SET customer_name = %s,
                    total_price = %s,
                    payment_method = %s
                WHERE order_id = %s
            """
            cursor.execute(update_query, (new_name, new_price, new_payment, order_id))
            conn.commit()

            print(f"Order id {order_id} is successfully updated.")


        if option==4:
            order_id=input("Enter order id to delete:")
            confirm=input("Are you sure you Want to delete (yes/No):").lower()
            if confirm=="yes":
                    cursor.execute("DELETE FROM order_items WHERE order_id=%s",(order_id,))
                    cursor.execute("DELETE FROM orders WHERE order_id=%s",(order_id,))
                    conn.commit()
                    print(f"Order id {order_id} is deleted successfully!")
            else:
                print("Delete Cancelled!")

        if option==5:
            cursor.execute("Select * from orders WHERE payment_method='cash' AND payment_status='pending'")
            rows=cursor.fetchall()
            print("Pending cash payments:")
            if not rows:
                print("No Pending cash payments!")
            else:
                for row in rows:
                    print(row)

        if option==6:
            order_id=input("Enter order id you want to mark payment as paid:")
            cursor.execute("""
                    UPDATE orders SET payment_status='paid' WHERE order_id=%s AND payment_method='cash' """,(order_id,))
            conn.commit()
            print(f"💸 Order id:{order_id} payment is successful.")
            print("❤️ Thanks for visiting our HALAL PALACE ")
            

        if option==7:
            order_id=input("Enter order id you want to mark switched payments to cash as paid:")
            cursor.execute("""
                UPDATE orders SET payment_status='paid' WHERE order_id=%s AND payment_note='UPI failed, Switched to cash' """,(order_id,))
            cursor.execute("""
                UPDATE orders SET payment_note='selected cash at counter' WHERE order_id=%s AND payment_note='UPI failed, Switched to cash' """,(order_id,))
            conn.commit()

            print(f"💸 Order id:{order_id} payment is successful.")
            print("❤️ Thanks for visiting our HALAL PALACE ")

        if option==8:
            print("Exiting Admin Panel")
            break


if __name__=="__main__":
    if admin_login():
        admin_pannel()

