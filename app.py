from flask import Flask, render_template, request, redirect, Response
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

    return render_template("index.html", rows=stuff)

@app.route("/word")
def word_info():
    word = request.args.get("w")
    if not word:
        return render_template("error.html", error="Invalid Word")

    with connect(DB_FILENAME) as conn:
        db = conn.cursor()
        row = db.execute(f"SELECT * FROM {TABLE_NAME} WHERE word = :word", {"word": word.lower()}).fetchone()
        if not row:
            return render_template("error.html", error="Invalid Word")

        return render_template("word.html", row=row)

@app.route("/add", methods=["GET", "POST"])
def add():
    method = request.method
    if method == "GET":
        return render_template("add.html")
    if method == "POST":
        word: str = request.form.get("word")
        definition = request.form.get("def")
        wordType = request.form.get("type").lower()

        # check word type
        if not wordType in ["adjective", "noun", "phrase", "adverb"]:
            return render_template("error.html", error="Invalid Word Type")

        with connect(DB_FILENAME) as conn:
            db = conn.cursor()
            result = db.execute(f"INSERT INTO {TABLE_NAME} (word, def, wordType) VALUES (?, ?, ?)", (word.lower(), definition, wordType))

        return redirect("/")

@app.route("/delete-word", methods=["DELETE"])
def delete():
    word_id = request.get_json(force=True).get("wordId")

    if not word_id:
        return Response({"error": "Invalid Word Id"}, status=400)

    with connect(DB_FILENAME) as conn:
        cursor = conn.cursor()
        result = cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = :word_id", {"word_id": word_id})
        return Response({"error": ""}, status=200)

@app.route("/edit/<word>", methods=["POST", "GET"])
def edit_word(word: str):
    if request.method == "POST":
        pass
    else:
        with connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            row = cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE word = :word", {"word": word}).fetchone()
            return render_template("edit.html", row=row)
