# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

#deploy
import os
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")


BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "users.db")

# ---------------- DB helpers ----------------
def get_db():
    if "db" not in g:
        # timeout gives SQLite a short wait if DB briefly locked
        g.db = sqlite3.connect(DB_PATH, timeout=15, check_same_thread=False)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    """Initialize DB. Creates file/table if missing and enables WAL mode."""
    first_time = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    try:
        # enable WAL to reduce locking issues
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        conn.commit()
    finally:
        conn.close()

# Initialize DB at startup
init_db()

# ---------------- Static currency data (offline) ----------------
CURRENCY_RATES = {
    "USD": 1.00, "EUR": 0.92, "GBP": 0.78, "INR": 83.00, "JPY": 146.00,
    "AUD": 1.52, "CAD": 1.36, "CNY": 7.25, "SGD": 1.34, "AED": 3.67
}
CURRENCY_CODES = list(CURRENCY_RATES.keys())

# ---------------- Routes ----------------
@app.route("/")
def root():
    if "username" in session:
        return redirect(url_for("converter"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Please fill both username and password.", "warning")
            return redirect(url_for("register"))

        db = get_db()
        # check if username exists
        row = db.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
        if row:
            flash("⚠️ Username already exists. Choose another.", "danger")
            return redirect(url_for("register"))

        # insert hashed password
        hashed = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            db.commit()
        except sqlite3.IntegrityError as e:
            # extremely unlikely due to race, but handle gracefully
            flash("⚠️ Username already exists. Choose another.", "danger")
            return redirect(url_for("register"))
        flash("✅ Successfully registered! Please login.", "success")
        # redirect to login with a query flag so login page can show an alert if you want
        return redirect(url_for("login", registered=1))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    registered_flag = request.args.get("registered") == "1"
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Please enter both username and password.", "warning")
            return redirect(url_for("login"))

        db = get_db()
        user = db.execute("SELECT id, username, password FROM users WHERE username = ?", (username,)).fetchone()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("converter"))
        else:
            flash("❌ Invalid username or password.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html", registered=registered_flag)

@app.route("/converter", methods=["GET", "POST"])
def converter():
    if "username" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    result = None
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount", "0"))
            from_cur = request.form.get("from_currency")
            to_cur = request.form.get("to_currency")
            if from_cur not in CURRENCY_RATES or to_cur not in CURRENCY_RATES:
                flash("Invalid currency selected.", "danger")
                return redirect(url_for("converter"))
            usd = amount / CURRENCY_RATES[from_cur]
            converted = round(usd * CURRENCY_RATES[to_cur], 2)
            result = f"{amount:.2f} {from_cur} = {converted:.2f} {to_cur}"
        except ValueError:
            flash("Amount must be a number.", "warning")
    return render_template("index.html", currencies=CURRENCY_CODES, result=result, username=session.get("username"))

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("login"))

# Run app (threaded=False to reduce DB lock risk in dev)
if __name__ == "__main__":
    app.run(debug=True)

