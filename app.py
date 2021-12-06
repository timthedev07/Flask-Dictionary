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

@app.route("/term")
def term_info():
    term = request.args.get("w")
    if not term:
        return render_template("error.html", error="Invalid Term")

    with connect(DB_FILENAME) as conn:
        db = conn.cursor()
        row = db.execute(f"SELECT * FROM {TABLE_NAME} WHERE term = :term", {"term": term.lower()}).fetchone()
        if not row:
            return render_template("error.html", error="Invalid term")

        return render_template("term.html", row=row)

@app.route("/add", methods=["GET", "POST"])
def add():
    method = request.method
    if method == "GET":
        return render_template("add.html")
    if method == "POST":
        term = request.form.get("term")
        definition = request.form.get("def")
        termType = request.form.get("type")

        if not term:
            return render_template("error.html", error="Invalid Term")
        if not definition:
            return render_template("error.html", error="Invalid Definition")
        if not termType:
            return render_template("error.html", error="Please Select The Appropriate Type")

        termType = termType.lower()

        # check term type
        if not termType in ["adjective", "noun", "phrase", "adverb", "verb"]:
            return render_template("error.html", error="Invalid Term Type")

        with connect(DB_FILENAME) as conn:
            db = conn.cursor()
            result = db.execute(f"INSERT INTO {TABLE_NAME} (term, def, termType) VALUES (?, ?, ?)", (term.lower(), definition, termType))

        return redirect(f"/term?w={term}")

@app.route("/delete-term", methods=["DELETE"])
def delete():
    term_id = request.get_json(force=True).get("termId")

    if not term_id:
        return Response({"error": "Invalid term Id"}, status=400)

    with connect(DB_FILENAME) as conn:
        cursor = conn.cursor()
        result = cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = :term_id", {"term_id": term_id})
        return Response({"error": ""}, status=200)

@app.route("/edit/<term>", methods=["POST", "GET"])
def edit_term(term: str):
    if request.method == "POST":
        new_term = request.form.get("term")
        new_definition = request.form.get("def")
        new_type = request.form.get("type")

        if not new_term:
            return render_template("error.html", error="Invalid term Entered")
        if not new_definition:
            return render_template("error.html", error="Invalid Definition Entered")
        if not new_type:
            return render_template("error.html", error="Invalid term Type Selected")

        with connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {TABLE_NAME} SET term = :term, def = :def, termType = :termType WHERE term = :search_term", {
                "term": new_term,
                "def": new_definition,
                "termType": new_type,
                "search_term": term
            })
            return redirect(f"/term?w={new_term}")
    else:
        with connect(DB_FILENAME) as conn:
            cursor = conn.cursor()
            row = cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE term = :term", {"term": term}).fetchone()
            return render_template("edit.html", row=row)

@app.route("/search")
def term_search():
    keyword = request.args.get("q")
    termType = request.args.get("t")

    if not keyword:
        return render_template("Invalid term")

    keyword = keyword.lower()

    with connect(DB_FILENAME) as conn:
        cursor = conn.cursor()
        sqlString = f"SELECT * FROM {TABLE_NAME} WHERE term LIKE :keyword"
        values = {"keyword": f"%{keyword}%"}
        if termType and termType != "":
            sqlString += " AND termType = :termType"
            values["termType"] = termType
        rows = cursor.execute(sqlString, values).fetchall()
        return render_template("searchResult.html", rows=rows, keyword=keyword, hasItems=len(rows) > 0, selectedType=termType)

