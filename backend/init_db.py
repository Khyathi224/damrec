import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT NOT NULL,
    description TEXT,
    location TEXT,
    image_path TEXT
)
''')

conn.commit()
conn.close()
print("Database initialized.")
