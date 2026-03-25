from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "portfolio.db"


# -------------------- DATABASE CONNECTION --------------------
def get_db():
    return sqlite3.connect(DB_NAME)


# -------------------- INITIALIZE DATABASE --------------------
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Profile Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            title TEXT NOT NULL,
            about TEXT NOT NULL
        )
    """)

    # Enquiry Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            submitted_at TEXT NOT NULL
        )
    """)

    # Insert Default Profile Data (only if empty)
    cursor.execute("SELECT COUNT(*) FROM profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO profile (name, title, about)
            VALUES (?, ?, ?)
        """, (
            "Adithya Manuraj",
            "Web Developer | Python Enthusiast",
            "I am a passionate web developer skilled in Python, HTML, SQL, and backend development."
        ))

    conn.commit()
    conn.close()


# -------------------- RUN DB SETUP --------------------
init_db()


# -------------------- HOME ROUTE --------------------
@app.route("/")
def home():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, title, about FROM profile LIMIT 1")
    profile = cursor.fetchone()

    conn.close()

    return render_template(
        "index.html",
        name=profile[0],
        title=profile[1],
        about=profile[2],
        phone="999977771",
        email="adithyamanuraj135@gmail.com",
        skills=["C", "C++", "Python", "SQL", "HTML"],
        certificates=[
            "MongoDB Database Admin Path",
            "Wadhwani Self Presentation",
            "Front-End Web Development – Infosys",
            "UiPath Agentic Automation Training",
            "Digital Engineering – NASSCOM"
        ],
        school="Vijaya HSS (2024)",
        college="Kristu Jayanti University (2028)",
        experience="Fresher"
    )


# -------------------- ENQUIRY ROUTE --------------------
@app.route("/enquiry", methods=["POST"])
def enquiry():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    submitted_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO enquiries (name, email, message, submitted_at) VALUES (?, ?, ?, ?)",
        (name, email, message, submitted_at)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -------------------- RUN APP --------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)