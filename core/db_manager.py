# # core/db_manager.py
# import sqlite3
# import os
# from typing import Optional, Dict, Any, List

# BASE_DIR = os.path.join(os.getcwd(), "database")

# DB_PATHS = {
#     "final": {
#         "invoice": os.path.join(BASE_DIR, "final_database", "invoice.db"),
#         "passenger": os.path.join(BASE_DIR, "final_database", "passenger.db"),
#         "flight": os.path.join(BASE_DIR, "final_database", "flight.db"),
#         "ticket": os.path.join(BASE_DIR, "final_database", "ticket.db"),
#     },
#     "draft": {
#         "invoice": os.path.join(BASE_DIR, "draft_database", "draft_invoice.db"),
#         "passenger": os.path.join(BASE_DIR, "draft_database", "draft_passenger.db"),
#         "flight": os.path.join(BASE_DIR, "draft_database", "draft_flight.db"),
#         "ticket": os.path.join(BASE_DIR, "draft_database", "draft_ticket.db"),
#     },
#     "deleted": {
#         "invoice": os.path.join(BASE_DIR, "delete_database", "deleted_invoice.db"),
#         "passenger": os.path.join(BASE_DIR, "delete_database", "deleted_passenger.db"),
#         "flight": os.path.join(BASE_DIR, "delete_database", "deleted_flight.db"),
#         "ticket": os.path.join(BASE_DIR, "delete_database", "deleted_ticket.db"),
#     }
# }

# class DatabaseManager:
#     def __init__(self, db_type: str = "final"):
#         if db_type not in DB_PATHS:
#             raise ValueError("db_type must be 'final', 'draft', or 'deleted'")
#         self.db_type = db_type
#         self.paths = DB_PATHS[db_type]

#     def _connect(self, db_name: str):
#         return sqlite3.connect(self.paths[db_name])

#     # -------------------------
#     # Insert functions
#     # -------------------------
#     def insert_passenger(self, data: Dict[str, Any]) -> int:
#         conn = self._connect("passenger")
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO passengers (name, address, contact_number) VALUES (?, ?, ?)",
#             (data["name"], data.get("address"), data.get("contact_number")),
#         )
#         passenger_id = cursor.lastrowid
#         conn.commit()
#         conn.close()
#         return passenger_id

#     def insert_flight(self, data: Dict[str, Any]) -> int:
#         conn = self._connect("flight")
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO flights (airline, flight_number, departure_from, arrival_to, departure_date, arrival_date) "
#             "VALUES (?, ?, ?, ?, ?, ?)",
#             (
#                 data["airline"],
#                 data["flight_number"],
#                 data["departure_from"],
#                 data["arrival_to"],
#                 data["departure_date"],
#                 data["arrival_date"],
#             ),
#         )
#         flight_id = cursor.lastrowid
#         conn.commit()
#         conn.close()
#         return flight_id

#     def insert_ticket(self, data: Dict[str, Any]) -> int:
#         conn = self._connect("ticket")
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO tickets (ticket_number, base_fare, other_tax, gst_hst, total_amount) VALUES (?, ?, ?, ?, ?)",
#             (
#                 data["ticket_number"],
#                 data["base_fare"],
#                 data.get("other_tax", 0),
#                 data.get("gst_hst", 0),
#                 data["total_amount"],
#             ),
#         )
#         ticket_id = cursor.lastrowid
#         conn.commit()
#         conn.close()
#         return ticket_id

#     def insert_invoice(self, data: Dict[str, Any]) -> int:
#         conn = self._connect("invoice")
#         cursor = conn.cursor()
#         cursor.execute(
#             "INSERT INTO invoices (agent_name, pnr_number, invoice_number, invoice_date, passenger_id, flight_id, ticket_id) "
#             "VALUES (?, ?, ?, ?, ?, ?, ?)",
#             (
#                 data["agent_name"],
#                 data["pnr_number"],
#                 data["invoice_number"],
#                 data["invoice_date"],
#                 data["passenger_id"],
#                 data["flight_id"],
#                 data["ticket_id"],
#             ),
#         )
#         invoice_id = cursor.lastrowid
#         conn.commit()
#         conn.close()
#         return invoice_id

#     # -------------------------
#     # Fetch invoices with related data
#     # -------------------------
#     def fetch_invoice(self, invoice_id: int) -> Optional[Dict[str, Any]]:
#         conn = self._connect("invoice")
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM invoices WHERE invoice_id = ?", (invoice_id,))
#         invoice = cursor.fetchone()
#         conn.close()
#         if not invoice:
#             return None

#         invoice_dict = {
#             "invoice_id": invoice[0],
#             "agent_name": invoice[1],
#             "pnr_number": invoice[2],
#             "invoice_number": invoice[3],
#             "invoice_date": invoice[4],
#             "passenger_id": invoice[5],
#             "flight_id": invoice[6],
#             "ticket_id": invoice[7],
#         }

#         # Fetch linked passenger
#         if invoice_dict["passenger_id"]:
#             conn = self._connect("passenger")
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM passengers WHERE passenger_id = ?", (invoice_dict["passenger_id"],))
#             passenger = cursor.fetchone()
#             conn.close()
#             invoice_dict["passenger"] = passenger

#         # Fetch linked flight
#         if invoice_dict["flight_id"]:
#             conn = self._connect("flight")
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM flights WHERE flight_id = ?", (invoice_dict["flight_id"],))
#             flight = cursor.fetchone()
#             conn.close()
#             invoice_dict["flight"] = flight

#         # Fetch linked ticket
#         if invoice_dict["ticket_id"]:
#             conn = self._connect("ticket")
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (invoice_dict["ticket_id"],))
#             ticket = cursor.fetchone()
#             conn.close()
#             invoice_dict["ticket"] = ticket

#         return invoice_dict

#     # -------------------------
#     # Move invoice between DB types (draft → final or final → deleted)
#     # -------------------------
#     def move_invoice(self, invoice_id: int, target_type: str):
#         if target_type not in DB_PATHS:
#             raise ValueError("target_type must be 'final', 'draft', or 'deleted'")

#         # Fetch current invoice with all linked data
#         invoice_data = self.fetch_invoice(invoice_id)
#         if not invoice_data:
#             return False

#         # Connect to target DBs
#         target_db = DatabaseManager(db_type=target_type)

#         # Insert passenger
#         if invoice_data.get("passenger"):
#             passenger = invoice_data["passenger"]
#             passenger_id = target_db.insert_passenger(
#                 {"name": passenger[1], "address": passenger[2], "contact_number": passenger[3]}
#             )
#         else:
#             passenger_id = None

#         # Insert flight
#         if invoice_data.get("flight"):
#             flight = invoice_data["flight"]
#             flight_id = target_db.insert_flight(
#                 {
#                     "airline": flight[1],
#                     "flight_number": flight[2],
#                     "departure_from": flight[3],
#                     "arrival_to": flight[4],
#                     "departure_date": flight[5],
#                     "arrival_date": flight[6],
#                 }
#             )
#         else:
#             flight_id = None

#         # Insert ticket
#         if invoice_data.get("ticket"):
#             ticket = invoice_data["ticket"]
#             ticket_id = target_db.insert_ticket(
#                 {
#                     "ticket_number": ticket[1],
#                     "base_fare": ticket[2],
#                     "other_tax": ticket[3],
#                     "gst_hst": ticket[4],
#                     "total_amount": ticket[5],
#                 }
#             )
#         else:
#             ticket_id = None

#         # Insert invoice in target DB
#         target_db.insert_invoice(
#             {
#                 "agent_name": invoice_data["agent_name"],
#                 "pnr_number": invoice_data["pnr_number"],
#                 "invoice_number": invoice_data["invoice_number"],
#                 "invoice_date": invoice_data["invoice_date"],
#                 "passenger_id": passenger_id,
#                 "flight_id": flight_id,
#                 "ticket_id": ticket_id,
#             }
#         )

#         # Delete invoice from current DB
#         self.delete_invoice(invoice_id)
#         return True

#     # -------------------------
#     # Delete invoice from current DB
#     # -------------------------
#     def delete_invoice(self, invoice_id: int):
#         # Delete linked passenger
#         conn = self._connect("invoice")
#         cursor = conn.cursor()
#         cursor.execute("SELECT passenger_id, flight_id, ticket_id FROM invoices WHERE invoice_id = ?", (invoice_id,))
#         result = cursor.fetchone()
#         if result:
#             passenger_id, flight_id, ticket_id = result
#             conn.close()

#             if passenger_id:
#                 conn = self._connect("passenger")
#                 cursor = conn.cursor()
#                 cursor.execute("DELETE FROM passengers WHERE passenger_id = ?", (passenger_id,))
#                 conn.commit()
#                 conn.close()

#             if flight_id:
#                 conn = self._connect("flight")
#                 cursor = conn.cursor()
#                 cursor.execute("DELETE FROM flights WHERE flight_id = ?", (flight_id,))
#                 conn.commit()
#                 conn.close()

#             if ticket_id:
#                 conn = self._connect("ticket")
#                 cursor = conn.cursor()
#                 cursor.execute("DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,))
#                 conn.commit()
#                 conn.close()

#         # Finally, delete the invoice itself
#         conn = self._connect("invoice")
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM invoices WHERE invoice_id = ?", (invoice_id,))
#         conn.commit()
#         conn.close()



# core/db_manager.py
import sqlite3
import os
from typing import Optional, Dict, Any

# -------------------------
# Paths to all databases
# -------------------------
BASE_DIR = os.path.join(os.getcwd(), "database")

DB_PATHS = {
    "final": {
        "invoice": os.path.join(BASE_DIR, "final_database", "invoice.db"),
        "passenger": os.path.join(BASE_DIR, "final_database", "passenger.db"),
        "flight": os.path.join(BASE_DIR, "final_database", "flight.db"),
        "ticket": os.path.join(BASE_DIR, "final_database", "ticket.db"),
    },
    "draft": {
        "invoice": os.path.join(BASE_DIR, "draft_database", "draft_invoice.db"),
        "passenger": os.path.join(BASE_DIR, "draft_database", "draft_passenger.db"),
        "flight": os.path.join(BASE_DIR, "draft_database", "draft_flight.db"),
        "ticket": os.path.join(BASE_DIR, "draft_database", "draft_ticket.db"),
    },
    "deleted": {
        "invoice": os.path.join(BASE_DIR, "delete_database", "deleted_invoice.db"),
        "passenger": os.path.join(BASE_DIR, "delete_database", "deleted_passenger.db"),
        "flight": os.path.join(BASE_DIR, "delete_database", "deleted_flight.db"),
        "ticket": os.path.join(BASE_DIR, "delete_database", "deleted_ticket.db"),
    }
}


class DatabaseManager:
    """
    Handles all database interactions for final, draft, and deleted invoices.
    Provides methods to insert, fetch, move, and delete invoices along with
    linked passenger, flight, and ticket details.
    """

    def __init__(self, db_type: str = "final"):
        if db_type not in DB_PATHS:
            raise ValueError("db_type must be 'final', 'draft', or 'deleted'")
        self.db_type = db_type
        self.paths = DB_PATHS[db_type]
        
        
    # -------------------------
    # Internal connection helper
    # -------------------------
    def _connect(self, db_name: str):
        """Return a sqlite3 connection for the given DB name."""
        return sqlite3.connect(self.paths[db_name])

    # -------------------------
    # Insert methods
    # -------------------------
    def insert_passenger(self, data: Dict[str, Any]) -> int:
        conn = self._connect("passenger")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO passengers (name, address, contact_number) VALUES (?, ?, ?)",
            (data["name"], data.get("address"), data.get("contact_number")),
        )
        passenger_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return passenger_id

    def insert_flight(self, data: Dict[str, Any]) -> int:
        conn = self._connect("flight")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO flights (airline, flight_number, departure_from, arrival_to, departure_date, arrival_date) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                data["airline"],
                data["flight_number"],
                data["departure_from"],
                data["arrival_to"],
                data["departure_date"],
                data["arrival_date"],
            ),
        )
        flight_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return flight_id

    def insert_ticket(self, data: Dict[str, Any]) -> int:
        conn = self._connect("ticket")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tickets (ticket_number, base_fare, other_tax, gst_hst, total_amount) VALUES (?, ?, ?, ?, ?)",
            (
                data["ticket_number"],
                data["base_fare"],
                data.get("other_tax", 0),
                data.get("gst_hst", 0),
                data["total_amount"],
            ),
        )
        ticket_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return ticket_id

    def insert_invoice(self, data: Dict[str, Any]) -> int:
        conn = self._connect("invoice")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO invoices (agent_name, pnr_number, invoice_number, invoice_date, passenger_id, flight_id, ticket_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                data["agent_name"],
                data["pnr_number"],
                data["invoice_number"],
                data["invoice_date"],
                data["passenger_id"],
                data["flight_id"],
                data["ticket_id"],
            ),
        )
        invoice_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return invoice_id

    # -------------------------
    # Fetch invoice with related details
    # -------------------------
    def fetch_invoice(self, invoice_id: int) -> Optional[Dict[str, Any]]:
        conn = self._connect("invoice")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM invoices WHERE invoice_id = ?", (invoice_id,))
        invoice = cursor.fetchone()
        conn.close()
        if not invoice:
            return None

        invoice_dict = {
            "invoice_id": invoice[0],
            "agent_name": invoice[1],
            "pnr_number": invoice[2],
            "invoice_number": invoice[3],
            "invoice_date": invoice[4],
            "passenger_id": invoice[5],
            "flight_id": invoice[6],
            "ticket_id": invoice[7],
        }

        # Fetch linked passenger
        if invoice_dict["passenger_id"]:
            conn = self._connect("passenger")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM passengers WHERE passenger_id = ?", (invoice_dict["passenger_id"],))
            passenger = cursor.fetchone()
            conn.close()
            invoice_dict["passenger"] = passenger

        # Fetch linked flight
        if invoice_dict["flight_id"]:
            conn = self._connect("flight")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flights WHERE flight_id = ?", (invoice_dict["flight_id"],))
            flight = cursor.fetchone()
            conn.close()
            invoice_dict["flight"] = flight

        # Fetch linked ticket
        if invoice_dict["ticket_id"]:
            conn = self._connect("ticket")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (invoice_dict["ticket_id"],))
            ticket = cursor.fetchone()
            conn.close()
            invoice_dict["ticket"] = ticket

        return invoice_dict

    # -------------------------
    # Move invoice to another DB type
    # -------------------------
    def move_invoice(self, invoice_id: int, target_type: str):
        if target_type not in DB_PATHS:
            raise ValueError("target_type must be 'final', 'draft', or 'deleted'")

        invoice_data = self.fetch_invoice(invoice_id)
        if not invoice_data:
            return False

        target_db = DatabaseManager(db_type=target_type)

        # Move passenger
        passenger_id = None
        if invoice_data.get("passenger"):
            passenger = invoice_data["passenger"]
            passenger_id = target_db.insert_passenger(
                {"name": passenger[1], "address": passenger[2], "contact_number": passenger[3]}
            )

        # Move flight
        flight_id = None
        if invoice_data.get("flight"):
            flight = invoice_data["flight"]
            flight_id = target_db.insert_flight(
                {
                    "airline": flight[1],
                    "flight_number": flight[2],
                    "departure_from": flight[3],
                    "arrival_to": flight[4],
                    "departure_date": flight[5],
                    "arrival_date": flight[6],
                }
            )

        # Move ticket
        ticket_id = None
        if invoice_data.get("ticket"):
            ticket = invoice_data["ticket"]
            ticket_id = target_db.insert_ticket(
                {
                    "ticket_number": ticket[1],
                    "base_fare": ticket[2],
                    "other_tax": ticket[3],
                    "gst_hst": ticket[4],
                    "total_amount": ticket[5],
                }
            )

        # Move invoice
        target_db.insert_invoice(
            {
                "agent_name": invoice_data["agent_name"],
                "pnr_number": invoice_data["pnr_number"],
                "invoice_number": invoice_data["invoice_number"],
                "invoice_date": invoice_data["invoice_date"],
                "passenger_id": passenger_id,
                "flight_id": flight_id,
                "ticket_id": ticket_id,
            }
        )

        # Delete original invoice
        self.delete_invoice(invoice_id)
        return True

    # -------------------------
    # Delete invoice and linked data
    # -------------------------
    def delete_invoice(self, invoice_id: int):
        conn = self._connect("invoice")
        cursor = conn.cursor()
        cursor.execute("SELECT passenger_id, flight_id, ticket_id FROM invoices WHERE invoice_id = ?", (invoice_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            passenger_id, flight_id, ticket_id = result

            if passenger_id:
                conn = self._connect("passenger")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM passengers WHERE passenger_id = ?", (passenger_id,))
                conn.commit()
                conn.close()

            if flight_id:
                conn = self._connect("flight")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM flights WHERE flight_id = ?", (flight_id,))
                conn.commit()
                conn.close()

            if ticket_id:
                conn = self._connect("ticket")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,))
                conn.commit()
                conn.close()

        # Delete invoice
        conn = self._connect("invoice")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM invoices WHERE invoice_id = ?", (invoice_id,))
        conn.commit()
        conn.close()

    # -------------------------
    # Check if invoice exists
    # -------------------------
    def invoice_exists(self, invoice_number: str) -> bool:
        conn = self._connect("invoice")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM invoices WHERE invoice_number=?", (invoice_number,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    # -------------------------
    # Get last invoice number for auto-generation
    # -------------------------
    def get_last_invoice_number(self) -> Optional[str]:
        """
        Returns the last invoice number stored in this DB type.
        Returns None if no invoices exist.
        """
        conn = self._connect("invoice")
        cursor = conn.cursor()
        cursor.execute("SELECT invoice_number FROM invoices ORDER BY invoice_id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None



