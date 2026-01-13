def insert_order(connection, order):
    cursor = connection.cursor()

    # Insert into orders table
    cursor.execute(
        "INSERT INTO orders (customer_name, total, datetime) VALUES (%s, %s, NOW()) RETURNING order_id",
        (order["customer_name"], order["total"])
    )

    order_id = cursor.fetchone()[0]

    # Insert each item into order_details
    for item in order["items"]:
        cursor.execute(
            "INSERT INTO order_details (order_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
            (order_id, item["product_id"], item["quantity"], item["total_price"])
        )

    connection.commit()
    cursor.close()
    return order_id



def get_all_orders(connection):
    cursor = connection.cursor()
    query = """
        SELECT order_id, customer_name, total, datetime
        FROM orders
        ORDER BY order_id DESC
    """
    cursor.execute(query)

    orders = []
    for (order_id, customer_name, total, datetime) in cursor:
        orders.append({
            "order_id": order_id,
            "customer_name": customer_name,
            "total": float(total),
            "datetime": datetime.strftime("%d-%m-%Y %H:%M")
        })

    cursor.close()
    return orders


