from database.db_config import get_connection

conn = get_connection()
if conn:
    print("Connected successfully!")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM STUDENT")
    count = cursor.fetchone()[0]
    print(f"Number of students: {count}")
    conn.close()
else:
    print("Failed to connect")