# Flask-Mongo-App
Project Structure:

```
flask_mongo_app/
│── app.py
│── templates/
│   ├── login.html
│   ├── forgot_password.html
│   ├── profile.html
│   ├── search_results.html
│── static/
│   ├── styles.css
│── requirements.txt
│── config.py
│── .env
```

### Installation Requirements

Before starting, install the required dependencies:

```sh
pip install -r requirements.txt
```

### requirements.txt

```
Flask
Flask-PyMongo
python-dotenv
Werkzeug
``` 

### config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/user_management')
```

### .env

```
SECRET_KEY=your_secret_key_here
MONGO_URI=mongodb://localhost:27017/user_management
EMAIL=your_email@example.com
EMAIL_PASSWORD=your_email_password
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
```

### Storing Data in MongoDB

The application stores user data in MongoDB. The `users` collection stores login details, while the `contacts` collection stores profile information.

`

### Steps to Run the Project

1. Clone the repository and navigate into the project folder:
   ```sh
   git clone your-repo-url.git
   cd flask_mongo_app
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up MongoDB and update `.env` with your database connection details.
4. Run the Flask application:
   ```sh
   python app.py
   ```
5. Open `http://127.0.0.1:5000/` in a browser.

This will allow user authentication, password reset, profile creation, and contact search functionalities with a styled UI.
