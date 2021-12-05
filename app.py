from flask import Flask, render_template
from sqlite3 import connect
from constants import TABLE_NAME

app = Flask(__name__)

@app.route("/")
def index():
    stuff = []

    with connect("db.db") as conn:
        db = conn.cursor()
        result = db.execute(f"SELECT * FROM {TABLE_NAME}")

        for row in result:
            stuff.append(row)
            print(row)

    return render_template("index.html", rows=stuff)