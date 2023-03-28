import mysql.connector
from tkinter import *
from tkinter import ttk
import csv


# Connect to the database
host = input("Enter the host: ")
user = input("Enter the user: ")
password = input("Enter the password: ")
database = input("Enter the database: ")

db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    auth_plugin="mysql_native_password"
)
cursor = db.cursor()

# Create the window
root = Tk()
root.title("Inventory Management System")
root.geometry("800x600")


columns = ("id", "name", "description", "price", "quantity", "category_id")

products_tree = ttk.Treeview(root, columns=columns, show="headings")
products_tree.place(x=50, y=50, width=400, height=500)

products_scrollbar_v = ttk.Scrollbar(
    root, orient="vertical", command=products_tree.yview)
products_scrollbar_v.place(x=450, y=50, height=500)
products_tree.configure(yscrollcommand=products_scrollbar_v.set)

products_scrollbar_h = ttk.Scrollbar(
    root, orient="horizontal", command=products_tree.xview)
products_scrollbar_h.place(x=50, y=550, width=400)
products_tree.configure(xscrollcommand=products_scrollbar_h.set)


products_tree["columns"] = columns

products_tree.column("id", width=50, anchor="center")
products_tree.column("name", width=100, anchor="center")
products_tree.column("description", width=100, anchor="center")
products_tree.column("price", width=100, anchor="center")
products_tree.column("quantity", width=100, anchor="center")
products_tree.column("category_id", width=100, anchor="center")


products_tree.heading("id", text="ID")
products_tree.heading("name", text="Name")
products_tree.heading("description", text="Description")
products_tree.heading("price", text="Price")
products_tree.heading("quantity", text="Quantity")
products_tree.heading("category_id", text="Category ID")

# Get the data from the database
cursor.execute("SELECT * FROM product")
products = cursor.fetchall()
for product in products:
    id = product[0]
    name = product[1]
    description = product[2]
    price = product[3]
    quantity = product[4]
    category_name = product[5]
    sql = "SELECT name FROM category WHERE id = %s"
    val = (category_name,)
    cursor.execute(sql, val)
    category_name = cursor.fetchone()[0]
    products_tree.insert(parent="", index="end", values=(
        id, name, description, price, quantity, category_name))

# Add a product
def add_product():

    name = name_entry.get()
    description = description_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()
    category = category_entry.get()

    sql = "INSERT INTO product (name, description, price, quantity, category_id) VALUES (%s, %s, %s, %s, %s)"
    val = (name, description, price, quantity, category)
    cursor.execute(sql, val)
    db.commit()

    sql = "SELECT name FROM category WHERE id = %s"
    val = (category,)
    cursor.execute(sql, val)
    category_name = cursor.fetchone()[0]

    products_tree.insert(parent="", index="end", values=(
        cursor.lastrowid, name, description, price, quantity, category_name))

    name_entry.delete(0, END)
    description_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    category_entry.delete(0, END)

# Modify a product
add_product_frame = Frame(root)
add_product_frame.place(x=500, y=50)
Label(add_product_frame, text="Name").grid(row=0, column=0)
name_entry = Entry(add_product_frame)
name_entry.grid(row=0, column=1)
Label(add_product_frame, text="Description").grid(row=1, column=0)
description_entry = Entry(add_product_frame)
description_entry.grid(row=1, column=1)
Label(add_product_frame, text="Price").grid(row=2, column=0)
price_entry = Entry(add_product_frame)
price_entry.grid(row=2, column=1)
Label(add_product_frame, text="Quantity").grid(row=3, column=0)
quantity_entry = Entry(add_product_frame)
quantity_entry.grid(row=3, column=1)
Label(add_product_frame, text="Category").grid(row=4, column=0)
category_entry = Entry(add_product_frame)
category_entry.grid(row=4, column=1)
add_product_button = Button(
    add_product_frame, text="Add Product", command=add_product)
add_product_button.grid(row=5, column=1)

# Delete a product
def delete_product():
    selection = products_tree.selection()
    if selection:
        product_id = products_tree.item(selection[0])["values"][0]
        sql = "DELETE FROM product WHERE id = %s"
        val = (product_id,)
        cursor.execute(sql, val)
        db.commit()
        products_tree.delete(selection[0])


delete_product_button = Button(
    root, text="Delete Product", command=delete_product)
delete_product_button.pack()

modify_product_frame = Frame(root)
modify_product_frame.place(x=500, y=250)
Label(modify_product_frame, text="ID").grid(row=0, column=0)
id_entry = Entry(modify_product_frame)
id_entry.grid(row=0, column=1)
Label(modify_product_frame, text="Name").grid(row=1, column=0)
name_entry2 = Entry(modify_product_frame)
name_entry2.grid(row=1, column=1)
Label(modify_product_frame, text="Description").grid(row=2, column=0)
description_entry2 = Entry(modify_product_frame)
description_entry2.grid(row=2, column=1)
Label(modify_product_frame, text="Price").grid(row=3, column=0)
price_entry2 = Entry(modify_product_frame)
price_entry2.grid(row=3, column=1)
Label(modify_product_frame, text="Quantity").grid(row=4, column=0)
quantity_entry2 = Entry(modify_product_frame)
quantity_entry2.grid(row=4, column=1)
Label(modify_product_frame, text="Category").grid(row=5, column=0)
category_entry2 = Entry(modify_product_frame)
category_entry2.grid(row=5, column=1)


def modify_product():
    product_id = id_entry.get()
    name = name_entry2.get()
    description = description_entry2.get()
    price = price_entry2.get()
    quantity = quantity_entry2.get()
    category = category_entry2.get()
    sql = "UPDATE product SET name = %s, description = %s, price = %s, quantity = %s, category_id = %s WHERE id = %s"
    val = (name, description, price, quantity, category, product_id)
    cursor.execute(sql, val)
    db.commit()
    products_tree.delete(*products_tree.get_children())
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    for product in products:
        products_tree.insert(parent="", index="end", values=product)
    id_entry.delete(0, END)
    name_entry2.delete(0, END)
    description_entry2.delete(0, END)
    price_entry2.delete(0, END)
    quantity_entry2.delete(0, END)
    category_entry2.delete(0, END)


modify_product_button = Button(
    modify_product_frame, text="Modify Product", command=modify_product)
modify_product_button.grid(row=6, column=1)

# Import to CSV
def import_to_csv():
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    cursor.execute("SELECT name FROM category")
    categories = cursor.fetchall()
    with open("./products.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["ID", "NAME", "DESCRIPTION",
                            "PRICE", "QUANTITY", "CATEGORY"])
        for product in products:
            id = product[0]
            name = product[1]
            description = product[2]
            price = product[3]
            quantity = product[4]
            category_id = product[5]
            category = categories[category_id - 1][0]
            product = [id, name, description, price, quantity, category]
            csv_writer.writerow(product)

# Export to CSV
import_to_csv_button = Button(
    root, text="Import to CSV", command=import_to_csv)
import_to_csv_button.pack()
import_to_csv_button.place(x=500, y=450)

root.mainloop()

db.close()