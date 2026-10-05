import pymysql

# Connect to MySQL
connection = pymysql.connect(
    host="host.docker.internal",    #host="127.0.0.1" and host.docker.internal 
    user="appuser",
    password="Shubham@6024",
    database="containerlocaldb",
    port=3306
)

try:
    cursor = connection.cursor()
    
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        )
    """)
    
    # Insert a sample row
    cursor.execute("INSERT INTO test_table (name) VALUES (%s)", ("Hello from Python!",))
    connection.commit()
    
    # Fetch and print rows
    cursor.execute("SELECT * FROM test_table")
    rows = cursor.fetchall()
    print("Data in test_table:")
    for row in rows:
        print(row)

finally:
    connection.close()
