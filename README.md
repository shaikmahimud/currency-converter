💱 Currency Converter Web App

A simple Flask-based Currency Converter web application with user login & registration system.
Built as a college project, it allows users to create an account, log in securely, and convert currencies using static conversion rates.

🚀 Features

🔐 User Authentication

Registration with username & password

Login system with session handling

Flash messages for errors/success

💱 Currency Conversion

Convert between 100+ world currencies

Uses static conversion rates (works offline)

🎨 Modern UI

Styled login/register pages (center aligned)

Popup success messages

Dark theme with white fonts for readability

🛠️ Tech Stack

Frontend: HTML, CSS (custom theme)

Backend: Python (Flask)

Database: SQLite (for storing users)

Deployment: PythonAnywhere / Render

📂 Project Structure
currencyconverter/
│── app.py                # Main Flask app
│── requirements.txt       # Project dependencies
│── users.db               # SQLite database (auto-created)
│── templates/
│     ├── index.html       # Currency converter page
│     ├── login.html       # Login page
│     └── register.html    # Register page
│── static/
      └── style.css        # Styling (optional)

⚡ Installation & Usage
1. Clone the Repository
git clone https://github.com/your-username/currencyconverter.git
cd currencyconverter

2. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run the Application
python3 app.py


Visit 👉 http://127.0.0.1:5000

🌍 Deployment

This project can be deployed on:

PythonAnywhere

Render

Heroku
 (with PostgreSQL if needed)

For PythonAnywhere:

Upload your files (app.py, templates/, static/, requirements.txt).

Create a virtual environment and install dependencies.

Configure WSGI file to point to app:app.

Reload the web app.

📸 Screenshots

👉 Login Page
👉 Register Page
👉 Converter Page

(Add screenshots here when you push to GitHub!)

👨‍💻 Author

Shaik Mahimud
Final Year B.Tech (AI & ML)
