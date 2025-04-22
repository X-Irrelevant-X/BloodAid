import sqlite3
from flask import *
from models import *
from urls import *
from werkzeug.security import *

def home():
    user_count = get_user_count()
    donor_count = get_donor_count()
    hospital_count = get_hospital_count()
    
    return render_template(
        'home.html',
        user_count=user_count,
        donor_count=donor_count,
        hospital_count=hospital_count
    )
    

def register():
    errors = {}

    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        contact = request.form['con']
        age = request.form['age']
        blood_group = request.form['blood_group']
        nid = request.form['nid']
        gender = request.form['gender']
        police_station = request.form['police_station']
        city = request.form['city']
        email = request.form['email']
        password = request.form['pass']

        # Validation
        errors = check_duplicate_fields(username, email, nid, contact)

        if len(password) < 8:
            errors['p'] = "*Password is too short"
        else:
            password = generate_password_hash(password)

        if not errors:
            user_data = {
                'name': name,
                'username': username,
                'contact': contact,
                'age': age,
                'blood_group': blood_group,
                'nid': nid,
                'gender': gender,
                'police_station': police_station,
                'city': city,
                'email': email,
                'password': password
            }

            insert_user(user_data)
            flash('Registered Successfully! Now you can proceed to login.', 'success')
            return redirect(url_for('login'))

        flash('Registration failed. See errors below.', 'danger')

    return render_template('register.html', errors=errors)


def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)

        if user and check_password_hash(user['pass'], password):
            session.clear()
            session['username'] = username
            return redirect('/userhome')
        else:
            error = "Invalid username or password"

    return render_template('login.html', error=error)


def logout():
    session.clear()
    return redirect(url_for('home'))


def user_home():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    
    # Get counts from the existing functions in models.py
    user_count = get_user_count()
    donor_count = get_donor_count()
    hospital_count = get_hospital_count()

    # Check if the user is a donor
    user = get_user_by_username(username)
    is_donor = bool(user) and 'donor_list' in user  # assuming there's a donor_list in user, adapt this

    return render_template('user_home.html',
                           user_count=user_count,
                           donor_count=donor_count,
                           hospital_count=hospital_count,
                           is_donor=is_donor)


def user_profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = get_user_by_username(session['username'])

    return render_template('user_profile.html', user=user)


def report_user():
    if request.method == 'POST':
        contact = request.form['contact']
        reason = request.form['reason']
        reported_by = session.get('username')

        if not user_exists_by_contact(contact):
            flash("None of our users have this contact number.", "error")
            return redirect(url_for('report_user'))

        submit_report(reported_by, contact, reason)
        flash("Report submitted successfully.", "success")
        return redirect(url_for('user_web_view'))

    return render_template('report_user.html')


def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_new_password']

        if new_password != confirm_password:
            flash("New passwords do not match!", "error")
            return redirect(request.url)

        user = get_user_by_username(username)
        if user and check_password_hash(user['pass'], current_password):
            new_hash = generate_password_hash(new_password)
            update_user_password(username, new_hash)
            flash("Password updated successfully!", "success")
            return redirect(url_for('user_profile'))  # or profile/dashboard
        else:
            flash("Current password is incorrect!", "error")

    return render_template('change_password.html')


def delete_account():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login page if not logged in

    if request.method == 'POST':
        username = session['username']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash("Passwords do not match!", "error")
            return redirect(request.url)

        # Retrieve user details from the database
        user = get_user_by_username(username)

        # Ensure the user exists and the provided password matches the stored hash
        if user and check_password_hash(user['pass'], password):  # Access by column name
            # Perform account deletion
            delete_user(username)
            session.clear()  # Clear session to log the user out
            flash("Sorry to see you go. Account deleted.", "success")
            return redirect(url_for('login'))  # Redirect to login after account deletion
        else:
            flash("Incorrect password!", "error")  # Show error if password is incorrect

    return render_template('delete_account.html')