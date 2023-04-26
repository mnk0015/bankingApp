from flask import Blueprint, render_template, redirect, request, session
from database import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/create_account", methods=["GET", "POST"])
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

@auth_bp.route("/login", methods=["GET", "POST"])
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

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")
