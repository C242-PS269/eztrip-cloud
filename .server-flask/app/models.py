from app.db import Database

def get_all_items():
    db = Database.get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    return cursor.fetchall()

def get_item_by_id(item_id):
    db = Database.get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    return cursor.fetchone()

def create_item(item):
    db = Database.get_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO items (name, description, price, quantity) VALUES (%s, %s, %s, %s)",
        (item.name, item.description, item.price, item.quantity)
    )
    db.commit()
    return cursor.lastrowid

def update_item(item_id, item):
    db = Database.get_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE items SET name=%s, description=%s, price=%s, quantity=%s WHERE id=%s",
        (item.name, item.description, item.price, item.quantity, item_id)
    )
    db.commit()

def delete_item(item_id):
    db = Database.get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    db.commit()
