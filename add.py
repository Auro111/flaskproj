
import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()

# Check if the column already exists
cursor.execute("PRAGMA table_info(annunci)")
columns = [column[1] for column in cursor.fetchall()]

if 'user_id' not in columns:
    # Add the user_id column
    cursor.execute("ALTER TABLE annunci ADD COLUMN user_id INTEGER REFERENCES utenti(id)")
    print("user_id column added successfully!")
else:
    print("user_id column already exists.")

# Commit the changes and close the connection
conn.commit()
conn.close()
