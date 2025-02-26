from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from models import UserModel, ContactModel, ResetModel
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import smtplib
import secrets

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Initialize MongoDB
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/user_management')
mongo = PyMongo(app)

# Initialize Models
user_model = UserModel(mongo)
contact_model = ContactModel(mongo)
reset_model = ResetModel(mongo)

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']

        if user_model.find_user_by_username(username):
            flash("Username already exists", "error")
        else:
            user_model.create_user(username, password, email)
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_model.find_user_by_username(username)

        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            return redirect(url_for('profile'))
        flash('Invalid credentials', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logs out the user and clears the session."""
    session.clear()  # Clears all session data
    flash("Logged out successfully", "success")  # Flash logout message
    return redirect(url_for('login'))  # Redirects to login page



@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Handles password reset requests."""
    if request.method == 'POST':
        email = request.form['email']
        user = mongo.db.users.find_one({'email': email})

        if user:
            reset_token = secrets.token_urlsafe(16)
            reset_model.create_reset_token(user['_id'], reset_token, expires_at=3600)
            
            # Send email
            send_reset_email(email, reset_token)
            flash("Password reset email sent", "success")
        else:
            flash("Email not found", "error")

    return render_template('forgot_password.html')


def send_reset_email(email, token):
    """Sends a password reset email."""
    sender_email = os.getenv('EMAIL')
    sender_password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))

    message = f"""Subject: Password Reset
    Click the link to reset your password: http://127.0.0.1:5000/reset_password/{token}
    """

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """Allows users to enter and view contact details."""
    if 'user_id' not in session:
        flash("You must log in first.", "error")
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    # Fetch user details from database
    user = user_model.find_user_by_id(user_id)
    
    if not user:
        flash("User not found!", "error")
        return redirect(url_for('login'))

    # Ensure we handle cases where 'registration_number' might be missing
    registration_number = user.get("registration_number", "")

    # Fetch user contact details
    contact = contact_model.find_by_registration(registration_number) if registration_number else None

    if request.method == 'POST':
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        registration_number = request.form['registration_number']

        contact_model.create_contact(user_id, phone, email, address, registration_number)
        flash("Profile updated successfully", "success")
        return redirect(url_for('profile'))  # Reload the page with new data

    return render_template('profile.html', user=user, contact=contact)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Searches for contact by registration number."""
    if request.method == 'POST':
        reg_no = request.form.get('registration_number', '').strip()

        if not reg_no:
            flash("Please enter a registration number", "error")
            return redirect(url_for('search'))

        contact = contact_model.find_by_registration(reg_no)

        if not contact:
            flash("No contact found for the given registration number.", "error")

        return render_template('search_results.html', contact=contact)

    return render_template('search.html')
