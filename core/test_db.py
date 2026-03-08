from db_manager import DatabaseManager
from datetime import date

def test_database():
    # ---------------------
    # Step 1: Connect to draft DB
    # ---------------------
    draft_db = DatabaseManager(db_type="draft")

    # ---------------------
    # Step 2: Insert sample passenger
    # ---------------------
    passenger_id = draft_db.insert_passenger({
        "name": "John Doe",
        "address": "123 Main St, City",
        "contact_number": "1234567890"
    })

    # ---------------------
    # Step 3: Insert sample flight
    # ---------------------
    flight_id = draft_db.insert_flight({
        "airline": "AirTest",
        "flight_number": "AT123",
        "departure_from": "CityA",
        "arrival_to": "CityB",
        "departure_date": "2025-09-25",
        "arrival_date": "2025-09-25"
    })

    # ---------------------
    # Step 4: Insert sample ticket
    # ---------------------
    ticket_id = draft_db.insert_ticket({
        "ticket_number": "TCKT001",
        "base_fare": 200.0,
        "other_tax": 20.0,
        "gst_hst": 10.0,
        "total_amount": 230.0
    })

    # ---------------------
    # Step 5: Insert sample invoice
    # ---------------------
    invoice_id = draft_db.insert_invoice({
        "agent_name": "Agent Smith",
        "pnr_number": "PNR001",
        "invoice_number": "INV001",
        "invoice_date": date.today().isoformat(),
        "passenger_id": passenger_id,
        "flight_id": flight_id,
        "ticket_id": ticket_id
    })

    print(f"✅ Draft invoice created with ID: {invoice_id}")

    # ---------------------
    # Step 6: Fetch the invoice from draft DB
    # ---------------------
    invoice_data = draft_db.fetch_invoice(invoice_id)
    print("Draft Invoice Data:")
    print(invoice_data)

    # ---------------------
    # Step 7: Move invoice to final DB
    # ---------------------
    draft_db.move_invoice(invoice_id, target_type="final")
    print(f"✅ Draft invoice {invoice_id} moved to final DB")

    # ---------------------
    # Step 8: Fetch from final DB to confirm
    # ---------------------
    final_db = DatabaseManager(db_type="final")
    invoice_data_final = final_db.fetch_invoice(invoice_id=1)  # first invoice in final DB will have ID=1
    print("Final Invoice Data:")
    print(invoice_data_final)


if __name__ == "__main__":
    test_database()
