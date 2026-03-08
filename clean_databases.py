# clean_databases.py
import os

# Base folder where your databases are stored
BASE_DIR = r"C:\Users\uchit\OneDrive\Desktop\IGS-PYSIDE-Rajan-New\database"

# Database subfolders
DB_FOLDERS = ["final_database", "draft_database", "delete_database"]

# Delete all .db files in these folders
for folder in DB_FOLDERS:
    folder_path = os.path.join(BASE_DIR, folder)
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".db"):
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
    else:
        print(f"Folder does not exist: {folder_path}")

print("Database cleanup completed.")
