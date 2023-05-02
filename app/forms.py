from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField
from wtforms.validators import DataRequired, Length, NumberRange

class CreateAccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    dob = StringField('Date of Birth', validators=[DataRequired(), Length(min=2, max=50)])
    pin = PasswordField('PIN', validators=[DataRequired(), Length(min=4, max=4)])

class LoginForm(FlaskForm):
    account_number = StringField('Account Number', validators=[DataRequired(), Length(min=4, max=4)])
    pin = PasswordField('PIN', validators=[DataRequired(), Length(min=4, max=4)])

class WithdrawForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])

class DepositForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])