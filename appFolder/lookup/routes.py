from lookup import app
from flask import render_template, redirect, url_for, flash
from lookup.models import Item, User
# from lookup.forms import RegisterForm, LoginForm, FullNameForm, ClearLogsButtonForm, AddACriminalForm, AddAnOfficerForm
from lookup.forms import *
from lookup import db
from flask_login import login_user, logout_user, login_required
from flask_mysqldb import MySQL
import mysql.connector
from datetime import datetime, date

def add_to_log(connObj, cursorObj, query):
    saved_query = query.replace("'", "")
    query_to_insert = f"{date.today()} at {datetime.now()} executed {saved_query}"
    insert_query = f"INSERT INTO Logs (query_run) VALUES ('{query_to_insert}')"
    cursorObj.execute(insert_query)
    connObj.commit()

mysqlapp = MySQL(app)
conn = mysql.connector.connect( user='root', password='2003', host='127.0.0.1', database='milestone3')
cursor = conn.cursor()

@app.route('/')
@app.route('/homepage')
def home_page():
    return render_template('homepage.html')

@app.route('/officers', methods = ['GET', 'POST'])
@login_required
def officers_page():
    conn = mysql.connector.connect( user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()
    person = FullNameForm()
    addOfficer = AddAnOfficerForm()
    deleteOfficer = DeleteAnOfficerForm()
    cols = "SHOW COLUMNS FROM Officers"
    coldata = cursor.execute(cols)
    colexe = cursor.fetchall()
    # print("PRINT", person.firstname.data and person.lastname.data)
    if person.firstname.data and person.lastname.data:
        query = f"SELECT * FROM Officers WHERE last LIKE '{person.lastname.data}' AND first LIKE '{person.firstname.data}'"
    elif person.firstname.data and not person.lastname.data:
        query = f"SELECT * FROM Officers WHERE first LIKE '{person.firstname.data}'"
    elif not person.firstname.data and person.lastname.data:
        query = f"SELECT * FROM Officers WHERE last LIKE '{person.lastname.data}'"
    else:
        query = "SELECT * From Officers"
    cursor.execute(query)
    data = cursor.fetchall()
    #Replaced with add_to_log() helper function
    #Add the query that was executed to the logging table
    # saved_query = query.replace("'", "") #remove conflicting apostrophes
    # insert_query = (f"INSERT INTO Logs (query_run) VALUES ('{date.today()} at {datetime.now()} executed {saved_query}')")
    # cursor.execute(insert_query)
    # conn.commit()
    #Replaced with add_to_log() helper function
    add_to_log(conn, cursor, query)
    if (addOfficer.firstname1.data and addOfficer.lastname1.data):
        new_officer_id_query = cursor.execute("SELECT MAX(Officer_ID) FROM Officers")
        new_officer_id = str(int(cursor.fetchone()[0]) + 1)
        print("new:", new_officer_id)
        #We will insert Precinct as '0000' by default
        query = f"INSERT INTO Officers (Officer_ID, First, Last, Precinct) VALUES ({(new_officer_id)}, '{addOfficer.firstname1.data}', '{addOfficer.lastname1.data}', '0000')"
        cursor.execute(query)
        conn.commit()
        add_to_log(conn, cursor, query)
    return render_template('officers.html', person=person, data=data, coldata=colexe, addOfficer=addOfficer, deleteOfficer=deleteOfficer)



@app.route('/criminals', methods = ['GET', 'POST'])
@login_required
def criminals_page():
    conn = mysql.connector.connect( user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()

    person = FullNameForm()
    addCriminal = AddACriminalForm()
    deleteCriminal = DeleteACriminalForm()
    cols = "SHOW COLUMNS FROM Criminals"
    coldata = cursor.execute(cols)
    colexe = cursor.fetchall()
    if person.firstname.data and person.lastname.data:
        query = f"SELECT * FROM Criminals WHERE last LIKE '{person.lastname.data}' AND first LIKE '{person.firstname.data}'"
    elif person.firstname.data and not person.lastname.data:
        query = f"SELECT * FROM Criminals WHERE first LIKE '{person.firstname.data}'"
    elif not person.firstname.data and person.lastname.data:
        query = f"SELECT * FROM Criminals WHERE last LIKE '{person.lastname.data}'"
    else:
        query = "SELECT * From Criminals"
    cursor.execute(query)
    data = cursor.fetchall()
    #Replaced with add_to_log() helper function
    # saved_query = query.replace("'", "") #remove conflicting apostrophes
    # insert_query = (f"INSERT INTO Logs (query_run) VALUES ('{date.today()} at {datetime.now()} executed {saved_query}')")
    # cursor.execute(insert_query)
    # conn.commit()
    #Replaced with add_to_log() helper function
    add_to_log(conn, cursor, query)
    return render_template('criminals.html', person=person, data=data, coldata=colexe, addCriminal=addCriminal, deleteCriminal=deleteCriminal)

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

@app.route('/logs', methods=['GET', 'POST'])
def logs_page():

    conn = mysql.connector.connect( user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()
    clear_logs_button = ClearLogsButtonForm()
    #Button was pressed, clear the log table
    if clear_logs_button.submit.data:
        query = "DROP TABLE Logs"
        cursor.execute(query)
        conn.commit()
        query = "CREATE TABLE Logs ( query_run VARCHAR(255))"
        cursor.execute(query)
        conn.commit()
    #If button wasn't pressed, log table remains unchanged
    cursor.execute("SELECT * from Logs")
    logs = cursor.fetchall()
    return render_template('logs.html', logs=logs, clear_logs_button=clear_logs_button)








