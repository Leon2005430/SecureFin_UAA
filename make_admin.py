import sqlite3

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

cursor.execute(
    """
    UPDATE users
    SET role='admin'
    WHERE username=?
    """,
    ("Tan Ali Ali",)
)

conn.commit()
conn.close()

print("Admin updated")