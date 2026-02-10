from flask import Flask, render_template
import sqlite3

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

    # Insert Default Data
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

        # Profile
        name=profile[0],
        title=profile[1],
        about=profile[2],

        # Contact
        phone="999977771",
        email="adithyamanuraj135@gmail.com",

        # Skills
        skills=[
            "C", "C++", "Python", "SQL", "HTML"
        ],

        # Certifications
        certificates=[
            "MongoDB Database Admin Path",
            "Wadhwani Self Presentation",
            "Front-End Web Development – Infosys",
            "UiPath Agentic Automation Training",
            "Digital Engineering – NASSCOM"
        ],

        # Education
        school="Vijaya HSS (2024)",
        college="Kristu Jayanti University (2028)",

        # Experience
        experience="Fresher"
    )


# -------------------- RUN APP --------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)



