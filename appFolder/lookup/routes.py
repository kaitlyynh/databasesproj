from lookup import app
from flask import render_template, redirect, url_for, flash
from lookup.models import Item, User
from lookup.forms import RegisterForm, LoginForm,  FullNameForm
from lookup import db
from flask_login import login_user, logout_user, login_required
from flask_mysqldb import MySQL
import mysql.connector


mysql = MySQL(app)


@app.route('/')
@app.route('/homepage')
def home_page():
    return render_template('homepage.html')

@app.route('/officers', methods = ['GET', 'POST'])
@login_required
def officers_page():
    person = FullNameForm()
    items = Item.query.all()
    # if form.validate_on_submit():
    #     return render_template('officers.html', items=items, form=form)
    return render_template('officers.html', items=items, person=person)


@app.route('/criminals', methods = ['GET', 'POST'])
@login_required
def criminals_page():
    person = FullNameForm()
    return render_template('criminals.html', person=person)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('officers_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Successfully logged in! Username: {attempted_user.username}', category='success')
            return redirect(url_for('officers_page'))
        else:
            flash('That Username and Password is not correct, please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/sql')
def sql_page():
    # conn = mysql.connect()
    # # cursor = mysql.connect()
    # cursor = mysql.get_db().cursor()
    # # cursor =conn.cursor()
    # # cursor.execute("SELECT * from criminals")
    # first_entry = cursor.fetchone()
    conn = mysql.connector.connect( user='root', password='2003', host='127.0.0.1', database='milestone3')
    first_entry = 's'
    # cur = mysql.connection.cursor()

    return render_template('sql.html', first_entry=first_entry)








