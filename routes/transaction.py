from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash

from utils.database import mysql

transaction = Blueprint("transaction", __name__)

@transaction.route("/transaction/<int:id>", methods=["GET", "POST"])
def transaction_page(id):
    cur = mysql.connection.cursor()

    # get account details
    cur.execute("SELECT * FROM accounts WHERE id=%s", [id])
    account = cur.fetchone()

    if request.method == "POST":
        amount = float(request.form["amount"])
        trans_type = request.form["trans_type"]

        if trans_type == "withdraw":
            if amount > account["balance"]:
                flash("Insufficient balance.")
                return redirect(url_for("transaction.transaction_page", id=id))

            new_balance = account["balance"] - amount
            cur.execute("UPDATE accounts SET balance=%s WHERE id=%s", [new_balance, id])

            # log transaction
            cur.execute("INSERT INTO transactions (account_id, amount, trans_type, trans_date) VALUES (%s, %s, %s, %s)",
                        [id, amount, "withdraw", datetime.now()])
            mysql.connection.commit()

            flash(f"You withdrew {amount}. You now have {new_balance} in your account.")
            return redirect(url_for("transaction.transaction_page", id=id))

        elif trans_type == "deposit":
            new_balance = account["balance"] + amount
            cur.execute("UPDATE accounts SET balance=%s WHERE id=%s", [new_balance, id])

            # log transaction
            cur.execute("INSERT INTO transactions (account_id, amount, trans_type, trans_date) VALUES (%s, %s, %s, %s)",
                        [id, amount, "deposit", datetime.now()])
            mysql.connection.commit()

            flash(f"You deposited {amount}. You now have {new_balance} in your account.")
            return redirect(url_for("transaction.transaction_page", id=id))

    cur.execute("SELECT * FROM transactions WHERE account_id=%s ORDER BY trans_date DESC", [id])
    transactions = cur.fetchall()

    return render_template("transaction.html", account=account, transactions=transactions)
