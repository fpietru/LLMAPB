from flask import Flask, render_template, request
from flask_scss import Scss
import sqlite3
from text2sql import process_npl
from datetime import datetime

app = Flask(__name__)
Scss(app)

def create_db():
    conn = sqlite3.connect("phonebook.db")
    c = conn.cursor()
    c.execute("""
              CREATE TABLE IF NOT EXISTS phonebook (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
              )""")
    conn.commit()
    conn.close()

def make_query(sql):
    conn = sqlite3.connect("phonebook.db")
    c = conn.cursor()
    c.execute(sql)
    res = c.fetchall()
    conn.commit()
    conn.close()

    operation = sql.split(" ", 1)[0]
    if operation == "INSERT":
        return "Inserted into Phone Book!"
    if operation == "UPDATE":
        return "Updated Phone Book!"
    if operation == "DELETE":
        return "Deleted from Phone Book!"

    return res


responses = []
pending = None

@app.route("/", methods=["POST", "GET"])
def index():
    global pending
    if request.method == "POST":
        if "accept" in request.form:
            if pending:
                time = datetime.now()
                try:
                    res = make_query(pending[1])
                    responses.insert(0, [time, pending[1], res])
                except Exception as e:
                    print(f"Error: {e}")
                pending = None
        elif "decline" in request.form:
            pending = None
        else:
            command = request.form.get("command")
            sql = process_npl(command)
            pending = (command, sql)

    return render_template("index.html", responses=responses, pending=pending)


if __name__ in "__main__":
    create_db()
    app.run(debug=True)