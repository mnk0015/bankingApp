from flask import Blueprint, render_template, redirect, request, url_for, session
from .database import get_db

account_bp = Blueprint('account', __name__)

@account_bp.route('/dashboard')
def dashboard():
    # Retrieve user information from session
    user_id = session.get('user_id')
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT name, balance FROM users WHERE id=?", (user_id,))
    user_info = cur.fetchone()
    name, balance = user_info
    
    return render_template('account/dashboard.html', name=name, balance=balance)

@account_bp.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        amount = request.form['amount']
        if float(amount) > 0:
            user_id = session.get('user_id')
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT balance FROM users WHERE id=?", (user_id,))
            balance = cur.fetchone()[0]
            if balance >= float(amount):
                new_balance = balance - float(amount)
                cur.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, user_id))
                db.commit()
                return render_template('account/transaction_success.html', message=f'You withdrew {amount}. You now have {new_balance} in your account.')
            else:
                return render_template('account/transaction_error.html', message='Insufficient funds')
        else:
            return render_template('account/transaction_error.html', message='Invalid amount')
    else:
        return render_template('account/withdraw.html')

@account_bp.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        amount = request.form['amount']
        if float(amount) > 0:
            user_id = session.get('user_id')
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT balance FROM users WHERE id=?", (user_id,))
            balance = cur.fetchone()[0]
            new_balance = balance + float(amount)
            cur.execute("UPDATE users SET balance=? WHERE id=?", (new_balance, user_id))
            db.commit()
            return render_template('account/transaction_success.html', message=f'You deposited {amount}. You now have {new_balance} in your account.')
        else:
            return render_template('account/transaction_error.html', message='Invalid amount')
    else:
        return render_template('account/deposit.html')

@account_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
