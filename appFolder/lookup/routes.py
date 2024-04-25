from lookup import app
from flask import render_template, redirect, url_for, flash, request, abort
from lookup.models import User
from lookup.forms import *
from lookup import db
from flask_login import login_user, logout_user, login_required, current_user
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
        query = "SELECT * FROM Officers WHERE last LIKE %s AND first LIKE %s"
        cursor.execute(query,(person.lastname.data, person.firstname.data))
    elif person.firstname.data and not person.lastname.data:
        query = "SELECT * FROM Officers WHERE first LIKE %s"
        cursor.execute(query,(person.firstname.data,))
    elif not person.firstname.data and person.lastname.data:
        query = "SELECT * FROM Officers WHERE last LIKE %s"
        cursor.execute(query,(person.lastname.data,))
    else:
        query = "SELECT * From Officers"
        cursor.execute(query)
    print("Hi there hi there hi there", query)
    data = cursor.fetchall()
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
        query = "SELECT * FROM Criminals WHERE last LIKE %s AND first LIKE %s"
        cursor.execute(query, (person.lastname.data, person.firstname.data))
    elif person.firstname.data and not person.lastname.data:
        query = "SELECT * FROM Criminals WHERE first LIKE %s"
        cursor.execute(query, (person.firstname.data,))
    elif not person.firstname.data and person.lastname.data:
        query = "SELECT * FROM Criminals WHERE last LIKE %s"
        cursor.execute(query, (person.lastname.data,))
    else:
        query = "SELECT * From Criminals"
        cursor.execute(query)
    data = cursor.fetchall()
    add_to_log(conn, cursor, query)
    # if addCriminal.firstname2.data and addCriminal.lastname2.data:
    #     new_criminal_id_query = cursor.execute("SELECT MAX(Criminal_ID) FROM Criminals")
    #     new_criminal_id = str(int(cursor.fetchone()[0]) + 1)
    #     print("new:", new_criminal_id)
    #     try:
    #         query = f"INSERT INTO Criminals (Criminal_ID, First, Last) VALUES ({(new_criminal_id)}, '{addCriminal.firstname2.data}', '{addCriminal.lastname2.data}')"
    #         cursor.execute(query)
    #         conn.commit()
    #         add_to_log(conn, cursor, query)
    #     except:
    #         add_to_log(conn, cursor, query + "failed recheck your params")
    # if deleteCriminal.firstname4.data and deleteCriminal.lastname4.data:
    #     #find ID of criminal to delete (if they exist), assuming no criminals have the same name
    #     query = f"SELECT Criminal_ID FROM Criminals WHERE first LIKE '{deleteCriminal.firstname4.data}' and last LIKE '{deleteCriminal.lastname4.data}'"
    #     cursor.execute(query)
    #     if cursor.fetchall() != []: #if there was a result (officer to delete exists!)
    #         target_id = cursor.fetchone()
    #         #set first and last name to 'None' to represent a "fired" employee
    #         query = f"UPDATE Criminals SET first = 'None', last = 'None' WHERE Criminal_ID = {target_id[0]}"
    #         cursor.execute(query)
    #         conn.commit()
    #         add_to_log(conn, cursor, query)
    #     else:
    #         query = query + f" failed to execute, Criminal {deleteCriminal.firstname4.data} {deleteCriminal.lastname4.data} does not exist"
    #         add_to_log(conn, cursor, query)
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
@login_required
def logs_page():

    conn = mysql.connector.connect( user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()
    clear_logs_button = ClearLogsButtonForm()
    #Button was pressed, clear the log table
    if "@gov.com" in current_user.email_address:
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
    flash("You do not have permission to access this page, you do not have .gov in your email address", category='danger')
    return redirect(url_for("home_page"))  # Redirect to home page or other appropriate action
#detail pages
@app.route('/officer/<int:officer_id>')
@login_required
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
@login_required
def criminal_info(criminal_id):
    conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()
    if "@gov.com" in current_user.email_address:
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
    flash("You do not have permission to access this page, you do not have .gov in your email address", category='danger')
    return redirect(url_for("home_page"))  # Redirect to home page or other appropriate action


@app.route('/add_officer', methods=['GET', 'POST'])
@login_required
def add_officer():  
    addOfficer = AddAnOfficerForm()
    # print("in here1")
    # print(addOfficer.data)
    if "@gov.com" in current_user.email_address:
        if addOfficer.validate_on_submit():
            print("in here")
            conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
            cursor = conn.cursor()
            new_officer_id_query = cursor.execute("SELECT MAX(Officer_ID) FROM Officers")
            print("precinct: ", addOfficer.precinct.data)
            new_officer_id = str(int(cursor.fetchone()[0]) + 1)
            try:
                query = "INSERT INTO Officers VALUES (%s,%s,%s,%s,%s,%s,%s)"
                params=(new_officer_id, addOfficer.firstname1.data,addOfficer.lastname1.data,addOfficer.precinct.data,addOfficer.badge.data, addOfficer.phone.data,addOfficer.status.data)
                cursor.execute(query,params)
                conn.commit()
                add_to_log(conn, cursor, query)
            except:
                add_to_log(conn, cursor, query + "failed to execute, please check your params")
    
        return render_template('add_officer.html', addOfficer=addOfficer)
    flash("You do not have permission to access this page, you do not have .gov in your email address", category='danger')
    return redirect(url_for("home_page"))  # Redirect to home page or other appropriate action

    

@app.route('/add_criminal', methods=['GET', 'POST'])
@login_required
def add_criminal():  
    addCriminal = AddACriminalForm()
    if "@gov.com" in current_user.email_address:
        if addCriminal.validate_on_submit():
            conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
            cursor = conn.cursor()
            new_criminal_id_query = cursor.execute("SELECT MAX(Criminal_ID) FROM Criminals")
            try:
                new_criminal_id = str(int(cursor.fetchone()[0]) + 1)
                query = "INSERT INTO Criminals VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                params = (new_criminal_id, addCriminal.firstname2.data, addCriminal.lastname2.data, addCriminal.street.data, addCriminal.city.data, addCriminal.state.data, addCriminal.zip.data, addCriminal.phone.data, addCriminal.v_stat.data, addCriminal.p_stat.data)
                # print(query)
                cursor.execute(query,params)
                conn.commit()
                add_to_log(conn, cursor, query)
            except:
                add_to_log(conn, cursor, query + "failed to execute, please check your params")

        return render_template('add_criminal.html', addCriminal=addCriminal)
    flash("You do not have permission to access this page, you do not have .gov in your email address", category='danger')
    return redirect(url_for("home_page"))  # Redirect to home page or other appropriate action


@app.route('/delete_officer/<int:officer_id>', methods=['POST'])
@login_required
def delete_officer(officer_id):
    conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()
    if "@gov.com" in current_user.email_address:
        try:
            cursor.execute("DELETE FROM Crime_officers WHERE Officer_ID = %s", (officer_id,))
            cursor.execute("DELETE FROM Officers WHERE Officer_ID = %s", (officer_id,))
            conn.commit()
        except Exception as e:
            print("Failed to delete officer:", e)
            conn.rollback()
            return "Error deleting officer", 500
        finally:
            cursor.close()
            conn.close()
    
        return redirect(url_for('officers_page'))    
    flash("You do not have permission to access this page, you do not have .gov in your email address", category='danger')
    return redirect(url_for("home_page"))  # Redirect to home page or other appropriate action



@app.route('/delete_criminal/<int:criminal_id>', methods=['POST'])
@login_required
def delete_criminal(criminal_id):
    conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()
    if "@gov.com" in current_user.email_address:
        try:
            # Delete associated records from dependent tables
            cursor.execute("DELETE FROM Crime_charges WHERE Crime_ID IN (SELECT Crime_ID FROM Crimes WHERE Criminal_ID = %s)", (criminal_id,))
            cursor.execute("DELETE FROM Appeals WHERE Crime_ID IN (SELECT Crime_ID FROM Crimes WHERE Criminal_ID = %s)", (criminal_id,))
            cursor.execute("DELETE FROM Sentences WHERE Criminal_ID = %s", (criminal_id,))
            cursor.execute("DELETE FROM Alias WHERE Criminal_ID = %s", (criminal_id,))
            cursor.execute("DELETE FROM Crimes WHERE Criminal_ID = %s", (criminal_id,))
            cursor.execute("DELETE FROM Criminals WHERE Criminal_ID = %s", (criminal_id,))
            conn.commit()
        except Exception as e:
            print("Failed to delete criminal:", e)
            conn.rollback()
            return "Error deleting criminal", 500
        finally:
            cursor.close()
            conn.close()
    
        return redirect(url_for('criminals_page'))
    flash("You do not have permission to access this page, you do not have .gov in your email address", category='danger')
    return redirect(url_for("home_page"))  # Redirect to home page or other appropriate action


@app.route('/cases', methods=['GET', 'POST'])
@login_required
def cases_page():
    form = CrimeSearchForm()
    crimes = None 
    specific_crime = None
    coldata = None

    conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()
    
    # Always fetch column data for the table headers
    cursor.execute("SHOW COLUMNS FROM Crimes")
    coldata = cursor.fetchall()

    if form.validate_on_submit():
        crime_id = form.crime_id.data
        cursor.execute("SELECT * FROM Crimes WHERE Crime_ID = %s", (crime_id,))
        specific_crime = cursor.fetchone()
    else:
        cursor.execute("SELECT * FROM Crimes")
        crimes = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template('cases.html', form=form, crimes=crimes, specific_crime=specific_crime, coldata=coldata)
@app.route('/probation_officer/<int:prob_id>')
def probation_officer_info(prob_id):
    conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Prob_officer WHERE Prob_ID = %s", (prob_id,))
        officer_details = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    if not officer_details:
        return "No probation officer found with ID: {}".format(prob_id), 404

    return render_template('probation_officer_info.html', officer=officer_details)

@app.route('/reduce_punishment', methods=['GET','POST'])
def reduce_punishment():
    appeal_id = request.form['appeal_id']
    if not appeal_id:
        flash("Appeal ID is missing!", "error")
        return redirect(url_for('home_page'))

    conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()
    try:
        cursor.callproc('ReducePunishment', [int(appeal_id)])
        conn.commit()
        flash("Punishment reduced successfully for Appeal ID: " + str(appeal_id), "success")
    except Exception as e:
        conn.rollback()
        flash("Failed to reduce punishment: " + str(e), "error")
    finally:
        cursor.close()
    return redirect(url_for('criminal_info', criminal_id=request.form['criminal_id']))

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update_page():  
    
    conn = mysql.connector.connect(user='root', password='2003', host='127.0.0.1', database='milestone3')
    cursor = conn.cursor()
    # cursor.execute(f"GRANT CREATE USER ON *.* TO 'root'@'localhost'")
    updateOfficer = OfficerUpdateForm()
    updateCriminal = CriminalUpdateForm()
    #Current user is a ".gov" user AKA an admin
    if "@gov.com" in current_user.email_address:
        #Grant Priveileges
        # cursor.execute(f"GRANT UPDATE ON milestone3.Officers TO '{current_user.username}'@'localhost'")
        # cursor.execute(f"GRANT UPDATE ON milestone3.Criminals TO '{current_user.username}'@'localhost'")
        # Apply changes
        cursor.execute("FLUSH PRIVILEGES")
        # Commit changes
        conn.commit()
        # User has the required email domain, proceed with rendering the page
        if updateOfficer.validate_on_submit():
            print("Here 1")
            if updateOfficer.target1.data == 'Status' and updateOfficer.new_data1.data not in ['A', 'I']:
                updateOfficer.new_data1.data = 'I' #make it inactive by default in case user enters an invalid enum value
            query = f"UPDATE Officers SET {updateOfficer.target1.data} = '{updateOfficer.new_data1.data}' WHERE Officer_ID = {updateOfficer.id1.data}"
            print(query)
            try:
                cursor.execute(query)
                conn.commit()
            except:
                query = "Update Officers Failed, recheck your params"
            add_to_log(conn, cursor, query)
        if updateCriminal.validate_on_submit():
            print("Here 2")
            if updateCriminal.target2.data in ["Violation Status", "Probation Status"]:
                if updateCriminal.new_data2.data not in ['Y', 'N']: #invalid v / p status response
                    print("Here 2.5")
                    add_to_log(conn, cursor, query + "failed to execute, check params")
                else: #valid v / p status response
                    print("Here 3")
                    query = f"UPDATE Criminals SET {updateCriminal.target2.data} = '{updateCriminal.new_data2.data}' WHERE Criminal_ID = {updateCriminal.id2.data}"
                    print(query)
                    try:
                        cursor.execute(query)
                        conn.commit()
                        add_to_log(conn, cursor, query)
                    except:
                        query = "Update Criminals failed to execute, recheck your params"
                        add_to_log(conn, cursor, query + "failed to execute, check params")
                    
            else: # not v or p status being edited
                print("Here 3")
                query = f"UPDATE Criminals SET {updateCriminal.target2.data} = '{updateCriminal.new_data2.data}' WHERE Criminal_ID = {updateCriminal.id2.data}"
                print(query)
                try:
                    cursor.execute(query)
                    conn.commit()
                except:
                    query = "Update Criminals failed to execute, recheck your params"
                add_to_log(conn, cursor, query)
        return render_template("update.html", updateOfficer=updateOfficer, updateCriminal=updateCriminal)
    # User does not have the required email domain, redirect or abort as needed
    # Commit changes
    flash("You do not have permission to access this page, you do not have .gov in your email address", category='danger')
    return redirect(url_for("home_page"))  # Redirect to home page or other appropriate action

