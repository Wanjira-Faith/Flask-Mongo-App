from flask_pymongo import PyMongo

class UserModel:
    """Handles user authentication and profile data."""

    def __init__(self, mongo: PyMongo):
        self.users = mongo.db.users

    def create_user(self, username, password_hash, email):
        """Creates a new user with hashed password."""
        user = {
            "username": username,
            "password": password_hash,
            "email": email
        }
        return self.users.insert_one(user)

    def find_user_by_username(self, username):
        """Finds a user by username."""
        return self.users.find_one({"username": username})


class ContactModel:
    """Handles user contact details."""

    def __init__(self, mongo: PyMongo):
        self.contacts = mongo.db.contacts

    def create_contact(self, user_id, phone, email, address, registration_number):
        """Stores user contact details."""
        contact = {
            "user_id": user_id,
            "phone": phone,
            "email": email,
            "address": address,
            "registration_number": registration_number
        }
        return self.contacts.insert_one(contact)

    def find_by_registration(self, registration_number):
        """Finds a contact by registration number."""
        return self.contacts.find_one({"registration_number": registration_number})


class ResetModel:
    """Handles password reset tokens."""

    def __init__(self, mongo: PyMongo):
        self.resets = mongo.db.password_resets

    def create_reset_token(self, user_id, reset_token, expires_at):
        """Stores a password reset token with expiration time."""
        reset_entry = {
            "user_id": user_id,
            "reset_token": reset_token,
            "expires_at": expires_at
        }
        return self.resets.insert_one(reset_entry)
