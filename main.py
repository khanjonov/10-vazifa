
import sqlite3

conn = sqlite3.connect('autosalon.db')
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand_id INTEGER,
    color TEXT,
    price REAL,
    FOREIGN KEY (brand_id) REFERENCES brands(id)
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    employee_id INTEGER,
    model_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (model_id) REFERENCES models(id)
);
""")
conn.commit()
print("Jadvallar muvaffaqiyatli yaratildi.")

def main():
    while True:
        print("\nQuyidagi buyruqlardan birini tanlang:")
        print("1. Barcha modellarni ko'rish")
        print("2. Xodimlar va buyurtmachilarning email'larini ko'rish")
        print("3. Har bir davlatda buyurtmachilar sonini ko'rish")
        print("4. Har bir davlatda xodimlar sonini ko'rish")
        print("5. Har bir brandda modellar sonini ko'rish")
        print("6. 5 tadan ko'p modellar mavjud bo'lgan brandlar")
        print("7. Buyurtmalarni barcha jadval bilan birlashtirish")
        print("8. Umumiy avtomobillar narxini chiqarish")
        print("9. Jami brandlar sonini chiqarish")
        print("10. Jadvalga ma'lumot qo'shish")
        print("0. Dasturni to'xtatish")
        
        choice = input("Tanlang: ")
        if choice == "0":
            break
        elif choice == "1":
            show_all_models()
        elif choice == "2":
            show_emails()
        elif choice == "3":
            show_customers_by_country()
        elif choice == "4":
            show_employees_by_country()
        elif choice == "5":
            show_models_by_brand()
        elif choice == "6":
            show_brands_with_many_models()
        elif choice == "7":
            join_orders_with_tables()
        elif choice == "8":
            show_total_model_price()
        elif choice == "9":
            show_total_brands()
        elif choice == "10":
            add_data()
        else:
            print("Noto'g'ri buyruq!")

main()

def show_all_models():
    cursor.execute("""
        SELECT models.name, brands.name, models.color 
        FROM models
        JOIN brands ON models.brand_id = brands.id
    """)
    results = cursor.fetchall()
    print("\nModellar:")
    for row in results:
        print(f"Model: {row[0]}, Brand: {row[1]}, Rangi: {row[2]}")

def show_emails():
    cursor.execute("""
        SELECT email FROM employees
        UNION
        SELECT email FROM customers
    """)
    results = cursor.fetchall()
    print("\nEmail'lar:")
    for email in results:
        print(email[0])

def show_customers_by_country():
    cursor.execute("""
        SELECT country, COUNT(*) as count 
        FROM customers 
        GROUP BY country 
        ORDER BY count DESC
    """)
    results = cursor.fetchall()
    print("\nHar bir davlatda buyurtmachilar soni:")
    for row in results:
        print(f"{row[0]}: {row[1]} ta")

def show_employees_by_country():
    cursor.execute("""
        SELECT country, COUNT(*) as count 
        FROM employees 
        GROUP BY country 
        ORDER BY count DESC
    """)
    results = cursor.fetchall()
    print("\nHar bir davlatda xodimlar soni:")
    for row in results:
        print(f"{row[0]}: {row[1]} ta")

def show_models_by_brand():
    cursor.execute("""
        SELECT brands.name, COUNT(models.id) as count 
        FROM brands
        JOIN models ON brands.id = models.brand_id
        GROUP BY brands.name
    """)
    results = cursor.fetchall()
    print("\nHar bir branddagi modellar soni:")
    for row in results:
        print(f"Brand: {row[0]}, Modellar soni: {row[1]}")

def show_brands_with_many_models():
    cursor.execute("""
        SELECT brands.name, COUNT(models.id) as count 
        FROM brands
        JOIN models ON brands.id = models.brand_id
        GROUP BY brands.name
        HAVING count > 5
    """)
    results = cursor.fetchall()
    print("\n5 tadan ko'p modellar mavjud bo'lgan brandlar:")
    for row in results:
        print(f"Brand: {row[0]}, Modellar soni: {row[1]}")

def join_orders_with_tables():
    cursor.execute("""
        SELECT orders.id, customers.name as customer, employees.name as employee, models.name as model 
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
        JOIN employees ON orders.employee_id = employees.id
        JOIN models ON orders.model_id = models.id
    """)
    results = cursor.fetchall()
    print("\nBuyurtmalar:")
    for row in results:
        print(f"Order ID: {row[0]}, Customer: {row[1]}, Employee: {row[2]}, Model: {row[3]}")

def show_total_model_price():
    cursor.execute("SELECT SUM(price) FROM models")
    total = cursor.fetchone()[0]
    print(f"\nUmumiy avtomobillar narxi: {total}")

def show_total_brands():
    cursor.execute("SELECT COUNT(*) FROM brands")
    total = cursor.fetchone()[0]
    print(f"\nJami brandlar soni: {total}")

def add_data():
    table = input("Qaysi jadvalga qo'shmoqchisiz (brands/models/employees/customers/orders)? ").strip().lower()
    if table == "brands":
        name = input("Brand nomi: ")
        cursor.execute("INSERT INTO brands (name) VALUES (?)", (name,))
    elif table == "models":
        name = input("Model nomi: ")
        brand_id = int(input("Brand ID: "))
        color = input("Rang: ")
        price = float(input("Narx: "))
        cursor.execute("INSERT INTO models (name, brand_id, color, price) VALUES (?, ?, ?, ?)", (name, brand_id, color, price))
    elif table == "employees":
        name = input("Xodim ismi: ")
        email = input("Email: ")
        country = input("Davlat: ")
        cursor.execute("INSERT INTO employees (name, email, country) VALUES (?, ?, ?)", (name, email, country))
    elif table == "customers":
        name = input("Buyurtmachi ismi: ")
        email = input("Email: ")
        country = input("Davlat: ")
        cursor.execute("INSERT INTO customers (name, email, country) VALUES (?, ?, ?)", (name, email, country))
    elif table == "orders":
        customer_id = int(input("Buyurtmachi ID: "))
       
