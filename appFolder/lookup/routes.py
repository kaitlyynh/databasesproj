from lookup import app
from flask import render_template, redirect, url_for, flash
from lookup.models import User
from lookup.forms import RegisterForm, LoginForm, FullNameForm, ButtonForm
from lookup import db
from flask_login import login_user, logout_user, login_required
from flask_mysqldb import MySQL
import mysql.connector


mysqlapp = MySQL(app)
conn = mysql.connector.connect( user='root', password='2003', host='127.0.0.1', database='milestone3')
cursor = conn.cursor()

@app.route('/')
@app.route('/homepage')
def home_page():
    return render_template('homepage.html')

# @app.route('/officers', methods = ['GET', 'POST'])
# @login_required
# def officers_page():
#     conn = mysql.connector.connect( user='root', password='2003', host='127.0.0.1', database='milestone3')
#     cursor = conn.cursor()

#     person = FullNameForm()
#     # submitted = ButtonForm()
#     # items = Item.query.all()

#     cols = "SHOW COLUMNS FROM Officers"
#     coldata = cursor.execute(cols)
#     colexe = cursor.fetchall()
#     print("PRINT", person.firstname.data and person.lastname.data)
#     if person.firstname.data and person.lastname.data:
#         query = f"SELECT * FROM Officers WHERE last LIKE '{person.lastname.data}' AND first LIKE '{person.firstname.data}'"
#     elif person.firstname.data and not person.lastname.data:
#         query = f"SELECT * FROM Officers WHERE first LIKE '{person.firstname.data}'"
#     elif not person.firstname.data and person.lastname.data:
#         query = f"SELECT * FROM Officers WHERE last LIKE '{person.lastname.data}'"
#     else:
#         query = "SELECT * From Officers"
#     print(query)
#     cursor.execute(query)
#     data = cursor.fetchall()
#     # print("Data: ", data)
#     return render_template('officers.html', person=person, data=data, coldata=colexe)
@app.route('/officers', methods=['GET', 'POST'])
@login_required
def officers_page():
    conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()

    person = FullNameForm()

    # Always fetch column data
    cols = "SHOW COLUMNS FROM Officers"
    cursor.execute(cols)
    coldata = cursor.fetchall()

    # Check if the form has been submitted and is valid
    if person.validate_on_submit():
        # Handle form submission
        conditions = []
        if person.firstname.data:
            conditions.append("first LIKE %s")
        if person.lastname.data:
            conditions.append("last LIKE %s")

        # Build the query based on conditions
        if conditions:
            query = f"SELECT * FROM Officers WHERE {' AND '.join(conditions)}"
            params = [f"%{person.firstname.data}%", f"%{person.lastname.data}%"] if person.firstname.data and person.lastname.data else [f"%{person.firstname.data or person.lastname.data}%"]
            cursor.execute(query, params)
        else:
            query = "SELECT * FROM Officers"
            cursor.execute(query)
        data = cursor.fetchall()
    else:
        # Default case when the form is not submitted, show all officers
        query = "SELECT * FROM Officers"
        cursor.execute(query)
        data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('officers.html', person=person, data=data, coldata=coldata)


@app.route('/criminals', methods = ['GET', 'POST'])
@login_required
def criminals_page():
    conn = mysql.connector.connect( user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()

    person = FullNameForm()

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
    return render_template('criminals.html', person=person, data=data, coldata=colexe)

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
    conn = mysql.connector.connect( user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()
    cursor.execute("SELECT * from Criminals")
    first_entry = cursor.fetchall()
    return render_template('sql.html', first_entry=first_entry)

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

    cursor.close()
    conn.close()

    return render_template('officer_details.html', officer=officer_details,crimes=crime_details)

from flask import render_template, request, abort

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





