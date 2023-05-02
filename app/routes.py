from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import CreateAccountForm, LoginForm, WithdrawForm, DepositForm
from app.models import User, db

bp = Blueprint('banking', __name__)

@bp.route('/')
def index():
    return render_template('login.html')

@bp.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = CreateAccountForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, dob=form.dob.data, pin=form.pin.data)
        db.session.add(user)
        db.session.commit()
        flash(f'New User created. Welcome {form.name.data}!', 'success')
        return redirect(url_for('banking.index'))
    return render_template('create_account.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.account_number.data, pin=form.pin.data).first()
        if user:
            return redirect(url_for('banking.home', user_id=user.id))
        else:
            flash('Invalid account number or PIN', 'danger')
    return render_template('login.html', form=form)

@bp.route('/home/<int:user_id>', methods=['GET', 'POST'])
def home(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('home.html', user=user)

@bp.route('/check_balance/<int:user_id>')
def check_balance(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('check_balance.html', user=user)

@bp.route('/withdraw/<int:user_id>', methods=['GET', 'POST'])
def withdraw(user_id):
    user = User.query.get_or_404(user_id)
    form = WithdrawForm()
    if form.validate_on_submit():
        if user.balance >= form.amount.data:
            user.balance -= form.amount.data
            db.session.commit()
            flash(f'You withdraw {form.amount.data}. You now have {user.balance} in your account.', 'success')
            return redirect(url_for('banking.home', user_id=user.id))
        else:
            flash('Insufficient balance', 'danger')
    return render_template('withdraw.html', user=user, form=form)

@bp.route('/deposit/<int:user_id>', methods=['GET', 'POST'])
def deposit(user_id):
    user = User.query.get_or_404(user_id)
    form = DepositForm()
    if form.validate_on_submit():
        user.balance += form.amount.data
        db.session.commit()
        flash(f'You deposited {form.amount.data}. You now have {user.balance} in your account.', 'success')
        return redirect(url_for('banking.home', user_id=user.id))
    return render_template('deposit.html', user=user, form=form)

@bp.route('/exit/<int:user_id>')
def exit(user_id):
    return redirect(url_for('banking.index'))