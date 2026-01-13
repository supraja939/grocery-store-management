def get_all_products(connection):
    cursor = connection.cursor()

    query = """
        SELECT 
            p.product_id,
            p.name,
            p.price_per_unit,
            u.uom_name
        FROM products p
        JOIN uom u ON p.uom_id = u.uom_id
        WHERE p.is_active = TRUE
        ORDER BY p.product_id
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    products = []
    for row in rows:
        products.append({
            "product_id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "uom_name": row[3]
        })

    cursor.close()
    return products




def insert_new_product(connection, product):
    cursor = connection.cursor()

    # Check if product already exists
    cursor.execute(
        "SELECT product_id, is_active FROM products WHERE LOWER(name) = LOWER(%s)",
        (product["name"],)
    )

    row = cursor.fetchone()

    if row:
        product_id, is_active = row

        if is_active:
            cursor.close()
            return "exists"   # already active

        # Reactivate old product
        cursor.execute(
            "UPDATE products SET is_active = TRUE, uom_id = %s, price_per_unit = %s WHERE product_id = %s",
            (product["uom_id"], product["price"], product_id)
        )

        connection.commit()
        cursor.close()
        return "reactivated"

    # Insert new product
    cursor.execute(
        "INSERT INTO products (name, uom_id, price_per_unit, is_active) VALUES (%s, %s, %s, TRUE)",
        (product["name"], product["uom_id"], product["price"])
    )

    connection.commit()
    cursor.close()
    return "created"




def delete_product(connection, product_id):
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE products SET is_active = FALSE WHERE product_id = %s AND is_active = TRUE",
        (product_id,)
    )

    rows = cursor.rowcount   # how many rows were updated
    connection.commit()
    cursor.close()

    return rows





