from lookup import app
from flask import render_template, redirect, url_for, flash, request, abort
from lookup.models import User
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
    cursor.execute(cols)
    coldata = cursor.fetchall()
    if person.firstname.data and person.lastname.data:
        query = f"SELECT * FROM Officers WHERE last LIKE '{person.lastname.data}' AND first LIKE '{person.firstname.data}'"
    elif person.firstname.data and not person.lastname.data:
        query = f"SELECT * FROM Officers WHERE first LIKE '{person.firstname.data}'"
    elif not person.firstname.data and person.lastname.data:
        query = f"SELECT * FROM Officers WHERE last LIKE '{person.lastname.data}'"
    else:
        query = "SELECT * From Officers"
    cursor.execute(query)
    print(query)
    data = cursor.fetchall()
    add_to_log(conn, cursor, query)
    # if addOfficer.firstname1.data and addOfficer.lastname1.data:
    #     new_officer_id_query = cursor.execute("SELECT MAX(Officer_ID) FROM Officers")
    #     new_officer_id = str(int(cursor.fetchone()[0]) + 1)
    #     print("new:", new_officer_id)
    #     #We will insert Precinct as '0000' by default
    #     query = f"INSERT INTO Officers (Officer_ID, First, Last, Precinct) VALUES ({(new_officer_id)}, '{addOfficer.firstname1.data}', '{addOfficer.lastname1.data}', '0000')"
    #     # cursor.execute(query)
    #     # conn.commit()
    #     add_to_log(conn, cursor, query)
    if deleteOfficer.firstname3.data and deleteOfficer.lastname3.data:
        #find ID of officer to delete (if they exist), assuming no officers have the same name
        query = f"SELECT Officer_ID FROM Officers WHERE first LIKE '{deleteOfficer.firstname3.data}' and last LIKE '{deleteOfficer.lastname3.data}'"
        cursor.execute(query)
        if cursor.fetchall() != []: #if there was a result (officer to delete exists!)
            target_id = cursor.fetchone()
            #set first and last name to 'None' to represent a "fired" employee
            query = f"UPDATE Officers SET first = 'None', last = 'None' WHERE Officer_ID = {target_id[0]}"
            # cursor.execute(query)
            # conn.commit()
            add_to_log(conn, cursor, query)
        else:
            query = query + f" failed to execute, Officer {deleteOfficer.firstname3.data} {deleteOfficer.lastname3.data} does not exist"
            add_to_log(conn, cursor, query)
    return render_template('officers.html', person=person, data=data, coldata=coldata, addOfficer=addOfficer, deleteOfficer=deleteOfficer)



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
    add_to_log(conn, cursor, query)
    if addCriminal.firstname2.data and addCriminal.lastname2.data:
        new_criminal_id_query = cursor.execute("SELECT MAX(Criminal_ID) FROM Criminals")
        new_criminal_id = str(int(cursor.fetchone()[0]) + 1)
        print("new:", new_criminal_id)
        query = f"INSERT INTO Criminals (Criminal_ID, First, Last) VALUES ({(new_criminal_id)}, '{addCriminal.firstname2.data}', '{addCriminal.lastname2.data}')"
        # cursor.execute(query)
        # conn.commit()
        add_to_log(conn, cursor, query)
    if deleteCriminal.firstname4.data and deleteCriminal.lastname4.data:
        #find ID of criminal to delete (if they exist), assuming no criminals have the same name
        query = f"SELECT Criminal_ID FROM Criminals WHERE first LIKE '{deleteCriminal.firstname4.data}' and last LIKE '{deleteCriminal.lastname4.data}'"
        cursor.execute(query)
        if cursor.fetchall() != []: #if there was a result (officer to delete exists!)
            target_id = cursor.fetchone()
            #set first and last name to 'None' to represent a "fired" employee
            query = f"UPDATE Criminals SET first = 'None', last = 'None' WHERE Criminal_ID = {target_id[0]}"
            # cursor.execute(query)
            # conn.commit()
            add_to_log(conn, cursor, query)
        else:
            query = query + f" failed to execute, Criminal {deleteCriminal.firstname4.data} {deleteCriminal.lastname4.data} does not exist"
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

#detail pages
@app.route('/officer/<int:officer_id>')
def officer_info(officer_id):
    conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()

    query = "SELECT * FROM Officers WHERE Officer_ID = %s"
    cursor.execute(query, (officer_id,))
    officer_details = cursor.fetchone()
    crime_query = """
    SELECT DISTINCT Crime_codes.Code_description
    FROM Crime_codes
    JOIN Crime_charges ON Crime_codes.Crime_code = Crime_charges.Crime_code
    JOIN Crimes ON Crime_charges.Crime_ID = Crimes.Crime_ID
    JOIN Crime_officers ON Crimes.Crime_ID = Crime_officers.Crime_ID
    WHERE Crime_officers.Officer_ID = %s;
    """
    cursor.execute(crime_query, (officer_id,))
    crime_details = cursor.fetchall()
    add_to_log(conn, cursor, "Join statements on Officer/Criminal Relations, Officer ID:" + str(officer_id))
    cursor.close()
    conn.close()

    return render_template('officer_details.html', officer=officer_details,crimes=crime_details)


@app.route('/criminal/<int:criminal_id>')
def criminal_info(criminal_id):
    conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Criminals WHERE Criminal_ID = %s", (criminal_id,))
        criminal_details = cursor.fetchone()

        cursor.execute("SELECT Alias FROM Alias WHERE Criminal_ID = %s", (criminal_id,))
        aliases = cursor.fetchall()

        cursor.execute("SELECT * FROM Sentences WHERE Criminal_ID = %s", (criminal_id,))
        sentences = cursor.fetchall()

        cursor.execute("""
        SELECT Appeals.* FROM Appeals
        JOIN Crimes ON Appeals.Crime_ID = Crimes.Crime_ID
        WHERE Crimes.Criminal_ID = %s;
        """, (criminal_id,))
        appeals = cursor.fetchall()

        cursor.execute("""
        SELECT Crime_charges.* FROM Crime_charges
        JOIN Crimes ON Crime_charges.Crime_ID = Crimes.Crime_ID
        WHERE Crimes.Criminal_ID = %s;
        """, (criminal_id,))
        crime_charges = cursor.fetchall()

        cursor.execute("""
        SELECT DISTINCT Prob_officer.Prob_ID, Prob_officer.Last, Prob_officer.First 
        FROM Prob_officer
        JOIN Sentences ON Prob_officer.Prob_ID = Sentences.Prob_ID
        WHERE Sentences.Criminal_ID = %s;
        """, (criminal_id,))
        probation_officers = cursor.fetchall()

        cursor.execute("""
        SELECT DISTINCT Officers.Officer_ID, Officers.Last, Officers.First
        FROM Officers
        JOIN Crime_officers ON Officers.Officer_ID = Crime_officers.Officer_ID
        JOIN Crimes ON Crime_officers.Crime_ID = Crimes.Crime_ID
        WHERE Crimes.Criminal_ID = %s;
        """, (criminal_id,))
        officers = cursor.fetchall()

        add_to_log(conn, cursor, "Join statements on Officer/Criminal Relations, Crim ID:" + str(criminal_id))

    except Exception as e:
        print("Error fetching data:", e)
        abort(404) 
    finally:
        cursor.close()
        conn.close()

    return render_template('criminal_info.html', 
                           criminal=criminal_details, 
                           aliases=aliases, 
                           sentences=sentences,
                           appeals=appeals,
                           crime_charges=crime_charges,
                           probation_officers=probation_officers,
                           officers=officers)

@app.route('/add_officer', methods=['GET', 'POST'])
def add_officer():  
    addOfficer = AddAnOfficerForm()
    # print("in here1")
    # print(addOfficer.data)
    if addOfficer.validate_on_submit():
        print("in here")
        conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
        cursor = conn.cursor()
        new_officer_id_query = cursor.execute("SELECT MAX(Officer_ID) FROM Officers")
        new_officer_id = str(int(cursor.fetchone()[0]) + 1)
        query = f"INSERT INTO Officers VALUES ({(new_officer_id)}, '{addOfficer.firstname1.data}', '{addOfficer.lastname1.data}', '{addOfficer.precinct.data}', '{addOfficer.badge.data}', '{addOfficer.phone.data}', {addOfficer.status.data}')"
        # cursor.execute(query)
        # conn.commit()
        add_to_log(conn, cursor, query)

    return render_template('add_officer.html', addOfficer=addOfficer)

@app.route('/add_criminal', methods=['GET', 'POST'])
def add_criminal():  
    addCriminal = AddACriminalForm()
    # print("in here1")
    # print(addOfficer.data)
    if addCriminal.validate_on_submit():
        print("in here")
        conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
        cursor = conn.cursor()
        new_criminal_id_query = cursor.execute("SELECT MAX(Criminal_ID) FROM Criminals")
        new_criminal_id = str(int(cursor.fetchone()[0]) + 1)
        query = f"INSERT INTO Criminals VALUES ({(new_criminal_id)}, '{addCriminal.firstname2.data}', '{addCriminal.lastname2.data}', '{addCriminal.street.data}', '{addCriminal.city.data}', '{addCriminal.state.data}', '{addCriminal.zip.data}', '{addCriminal.phone.data}', '{addCriminal.v_stat.data}', '{addCriminal.p_stat.data}')"
        cursor.execute(query)
        conn.commit()
        add_to_log(conn, cursor, query)

    return render_template('add_criminal.html', addCriminal=addCriminal)


