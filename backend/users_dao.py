def validate_user(connection, username, password):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT user_id FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cursor.fetchone()
    cursor.close()
    return user
