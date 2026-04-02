import sqlite3

def create_db():
    # Connect to (or create) the database file
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the table for people's data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS premium_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            upi_id TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database 'users.db' created successfully in VS Code!")

if __name__ == "__main__":
    create_db()
