import sqlite3
import os

db_path = os.path.join('instance', 'skillgap.db')

if os.path.exists(db_path):
    print(f"Connecting to {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(analyses)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'all_skills_json' not in columns:
            print("Adding all_skills_json column to analyses table...")
            cursor.execute("ALTER TABLE analyses ADD COLUMN all_skills_json TEXT")
            conn.commit()
            print("Successfully added column.")
        else:
            print("Column all_skills_json already exists.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
else:
    print(f"Database not found at {db_path}")
