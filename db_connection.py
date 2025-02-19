import mysql.connector

def get_db_connection():
    """Establish and return a database connection with a cursor."""
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '#Chowdary@536',
        'database': 'excel_data'
    }

    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Database connection successful!")
            return connection, connection.cursor(dictionary=True)
        else:
            print("Failed to establish a database connection.")
            return None, None
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None, None
