import psycopg2
def get_sql_connection():
    return psycopg2.connect(
        host="localhost",
        database="grocery_store",
        user="postgres",
        password="postgres",
        port="5432"
    )
