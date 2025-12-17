import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import create_user, verify_user, initialize_db

initialize_db()

username = input("Enter new username: ")
password = input("Enter new password: ")

create_user(username, password)
print(f"User '{username}' created successfully.")