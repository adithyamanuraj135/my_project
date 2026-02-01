from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY,
            name TEXT,
            title TEXT,
            about TEXT
        )
    """)

    # Insert data if table is empty
    c.execute("SELECT COUNT(*) FROM profile")
    if c.fetchone()[0] == 0:
        c.execute("""
            INSERT INTO profile (name, title, about)
            VALUES (?, ?, ?)
        """, (
            "Adithya Manuraj",
            "Web Developer | Python Enthusiast",
            "I am a passionate web developer with experience in HTML, CSS, and Python."
        ))

    conn.commit()
    conn.close()


# Run DB setup
init_db()


@app.route("/")
def home():

    conn = sqlite3.connect("portfolio.db")
    c = conn.cursor()

    c.execute("SELECT name, title, about FROM profile LIMIT 1")
    data = c.fetchone()

    conn.close()

    return render_template(
        "index.html",
        name=data[0],
        title=data[1],
        about=data[2]
    )


if __name__ == "__main__":
    app.run(debug=True)
