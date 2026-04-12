import oracledb

# THICK MODE – REQUIRED FOR ORACLE 11g
oracledb.init_oracle_client()

DB_USER = "placement_admin"
DB_PASSWORD = "YourStrongPassword"   # use YOUR actual password
DB_HOST = "localhost"
DB_PORT = "1521"
DB_SERVICE = "XE"

connection_string = f"{DB_USER}/{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SERVICE}"

def get_connection():
    try:
        connection = oracledb.connect(connection_string)
        print("✅ Database connection successful!")
        return connection
    except oracledb.Error as e:
        print(f"❌ Connection error: {e}")
        return None