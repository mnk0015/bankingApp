from flask import Flask, render_template, redirect, request, session
from flask_mysqldb import MySQL
from datetime import datetime
from functools import wraps
from database import db

app = Flask(__name__)
app.secret_key = "secret-key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        name = request.form["name"]
        dob = datetime.strptime(request.form["dob"], "%Y-%m-%d").date()
        pin = request.form["pin"]
        user_id = db.insert_user(name, dob, pin)
        db.insert_account(user_id)
        session["user_id"] = user_id
        return redirect("/account")

    return render_template("create_account.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pin = request.form["pin"]
        user = db.get_user_by_pin(pin)
        if user:
            session["user_id"] = user[0]
            return redirect("/account")
        else:
            return render_template("login.html", error="Invalid PIN")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/account")
@login_required
def account():
    user = db.get_user_by_id(session["user_id"])
    account = db.get_account_by_user_id(user[0])
    return render_template("account.html", user=user, account=account)

if __name__ == "__main__":
    app.run(debug=True)
