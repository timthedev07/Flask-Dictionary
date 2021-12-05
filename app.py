from flask import Flask, render_template, request, redirect
from sqlite3 import connect
from constants import TABLE_NAME, DB_FILENAME


app = Flask(__name__)

@app.route("/")
def index():
    stuff = []

    with connect(DB_FILENAME) as conn:
        db = conn.cursor()
        result = db.execute(f"SELECT * FROM {TABLE_NAME}")

        for row in result:
            stuff.append(row)
            print(row)

    return render_template("index.html", rows=stuff)

@app.route("/add", methods=["GET", "POST"])
def add():
    method = request.method
    if method == "GET":
        return render_template("add.html")
    if method == "POST":
        word = request.form.get("word")
        definition = request.form.get("def")

        with connect(DB_FILENAME) as conn:
            db = conn.cursor()
            result = db.execute(f"INSERT INTO {TABLE_NAME} (word, def) VALUES (?, ?)", (word, definition))

        return redirect("/")