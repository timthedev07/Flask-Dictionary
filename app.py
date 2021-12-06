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
        word = request.form.get("word")
        definition = request.form.get("def")
        wordType = request.form.get("type")

        if not word:
            return render_template("error.html", error="Invalid Word")
        if not definition:
            return render_template("error.html", error="Invalid Definition")
        if not wordType:
            return render_template("error.html", error="Please Select The Appropriate Type")

        wordType = wordType.lower()

        # check word type
        if not wordType in ["adjective", "noun", "phrase", "adverb"]:
            return render_template("error.html", error="Invalid Word Type")

        with connect(DB_FILENAME) as conn:
            db = conn.cursor()
            result = db.execute(f"INSERT INTO {TABLE_NAME} (word, def, wordType) VALUES (?, ?, ?)", (word.lower(), definition, wordType))

        return redirect(f"/word?w={word}")

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
        new_word = request.form.get("word")
        new_definition = request.form.get("def")
        new_type = request.form.get("type")

        if not new_word:
            return render_template("error.html", error="Invalid Word Entered")
        if not new_definition:
            return render_template("error.html", error="Invalid Definition Entered")
        if not new_type:
            return render_template("error.html", error="Invalid Word Type Selected")

        with connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {TABLE_NAME} SET word = :word, def = :def, wordType = :wordType WHERE word = :search_word", {
                "word": new_word,
                "def": new_definition,
                "wordType": new_type,
                "search_word": word
            })
            return redirect(f"/word?w={new_word}")
    else:
        with connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            row = cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE word = :word", {"word": word}).fetchone()
            return render_template("edit.html", row=row)
