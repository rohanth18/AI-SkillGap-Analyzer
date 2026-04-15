import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('instance/skillgap.db')
cursor = conn.cursor()

try:
    # Add ats_score column to analyses table
    print("Adding ats_score column to analyses table...")
    cursor.execute("ALTER TABLE analyses ADD COLUMN ats_score INTEGER DEFAULT 0")
    print("Column added successfully.")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
    print("Column might already exist.")

# Commit changes and close connection
conn.commit()
conn.close()
