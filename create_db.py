import sqlite3

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

id INTEGER PRIMARY KEY AUTOINCREMENT,

fullname TEXT NOT NULL,

username TEXT UNIQUE NOT NULL,

email TEXT NOT NULL,

password TEXT NOT NULL,

role TEXT DEFAULT 'customer'

)
""")

conn.commit()
conn.close()

print("Database Created Successfully")