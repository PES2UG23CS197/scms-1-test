from db.connection import get_connection

# PRODUCT FUNCTIONS
def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def add_product(sku, name, description, threshold):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Products (sku, name, description, threshold) VALUES (%s, %s, %s, %s)",
                   (sku, name, description, threshold))
    conn.commit()
    cursor.close()
    conn.close()

def update_product(sku, name, description, threshold):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Products SET name=%s, description=%s, threshold=%s WHERE sku=%s",
                   (name, description, threshold, sku))
    conn.commit()
    cursor.close()
    conn.close()

def delete_product(sku):
    conn = get_connection()
    cursor = conn.cursor()

    # First delete inventory entries that reference this SKU
    cursor.execute("DELETE FROM Inventory WHERE sku = %s", (sku,))

    # Then delete the product
    cursor.execute("DELETE FROM Products WHERE sku = %s", (sku,))
    
    conn.commit()
    cursor.close()
    conn.close()

# INVENTORY FUNCTIONS
def get_inventory():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Inventory.inventory_id, Inventory.sku, Inventory.location, Inventory.quantity,
               Products.threshold, Products.name
        FROM Inventory
        JOIN Products ON Inventory.sku = Products.sku
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def add_inventory(sku, location, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Inventory (sku, location, quantity) VALUES (%s, %s, %s)",
                   (sku, location, quantity))
    conn.commit()
    cursor.close()
    conn.close()

def update_inventory(sku, location, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Inventory
        SET quantity = %s, location = %s
        WHERE sku = %s
    """, (quantity, location, sku))
    conn.commit()
    cursor.close()
    conn.close()

def get_low_stock():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Inventory.sku, Products.name, Inventory.location, Inventory.quantity, Products.threshold
        FROM Inventory
        JOIN Products ON Inventory.sku = Products.sku
        WHERE Inventory.quantity < Products.threshold
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_products_by_warehouse(location):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Inventory.sku, Products.name, Inventory.quantity
        FROM Inventory
        JOIN Products ON Inventory.sku = Products.sku
        WHERE Inventory.location = %s
    """, (location,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
