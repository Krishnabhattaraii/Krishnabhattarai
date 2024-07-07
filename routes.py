from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from forms import RegistrationForm, LoginForm, IncomeForm, ExpenseForm
from models import User, Income, Expense
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/income', methods=['GET', 'POST'])
@login_required
def income():
    form = IncomeForm()
    if form.validate_on_submit():
        income = Income(amount=form.amount.data, category=form.category.data, author=current_user)
        db.session.add(income)
        db.session.commit()
        flash('Income has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('income.html', title='Add Income', form=form)

@app.route('/expense', methods=['GET', 'POST'])
@login_required
def expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(amount=form.amount.data, category=form.category.data, author=current_user)
        db.session.add(expense)
        db.session.commit()
        flash('Expense has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('expense.html', title='Add Expense', form=form)
