# core/db_init.py
import sqlite3
import os

# Base path for database folder (project_root/database)
BASE_DIR = os.path.join(os.getcwd(), "database")

# Database groups and filenames
DB_GROUPS = {
    "final_database": ["invoice.db", "passenger.db", "flight.db", "ticket.db"],
    "draft_database": ["draft_invoice.db", "draft_passenger.db", "draft_flight.db", "draft_ticket.db"],
    "delete_database": ["deleted_invoice.db", "deleted_passenger.db", "deleted_flight.db", "deleted_ticket.db"],
}

# Schema definitions for each table type
SCHEMAS = {
    "invoice": """
    CREATE TABLE IF NOT EXISTS invoices (
        invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_name TEXT NOT NULL,
        pnr_number TEXT NOT NULL,
        invoice_number TEXT UNIQUE NOT NULL,
        invoice_date DATE NOT NULL,
        passenger_id INTEGER,
        flight_id INTEGER,
        ticket_id INTEGER
    );
    """,
    "passenger": """
    CREATE TABLE IF NOT EXISTS passengers (
        passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT,
        contact_number TEXT
    );
    """,
    "flight": """
    CREATE TABLE IF NOT EXISTS flights (
        flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
        airline TEXT NOT NULL,
        flight_number TEXT NOT NULL,
        departure_from TEXT NOT NULL,
        arrival_to TEXT NOT NULL,
        departure_date DATE NOT NULL,
        arrival_date DATE NOT NULL
    );
    """,
    "ticket": """
    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_number TEXT UNIQUE NOT NULL,
        base_fare REAL NOT NULL,
        other_tax REAL DEFAULT 0,
        gst_hst REAL DEFAULT 0,
        total_amount REAL NOT NULL
    );
    """
}

def create_databases():
    for group, db_files in DB_GROUPS.items():
        folder = os.path.join(BASE_DIR, group)
        os.makedirs(folder, exist_ok=True)

        for db_file in db_files:
            db_path = os.path.join(folder, db_file)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Select schema by filename substring
            if "invoice" in db_file:
                cursor.executescript(SCHEMAS["invoice"])
            elif "passenger" in db_file:
                cursor.executescript(SCHEMAS["passenger"])
            elif "flight" in db_file:
                cursor.executescript(SCHEMAS["flight"])
            elif "ticket" in db_file:
                cursor.executescript(SCHEMAS["ticket"])

            conn.commit()
            conn.close()
            print(f"Initialized: {db_path}")

if __name__ == "__main__":
    create_databases()
    print("✅ All databases created successfully.")

