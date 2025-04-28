import sqlite3
from flask import *
from models import *
from urls import *
from werkzeug.security import *
from datetime import *

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
        admin = get_admin_by_username(username)

        if user:
            if any(val is None for val in [
                user['name'],
                user['contact'],
                user['email'],
                user['age'],
                user['blood_group'],
                user['nid'],
                user['gender'],
                user['police_station'],
                user['city']
            ]):
                error = "Decryption failed. Unauthorized Access."
                return render_template('login.html', error=error)

            if not check_password_hash(user['password'], password):
                error = "Invalid username or password."
                return render_template('login.html', error=error)

            # Set session for user login
            session['username'] = user['username']
            return redirect(url_for('user_home'))

        elif admin:
            if not check_password_hash(admin['pass'], password):
                error = "Invalid username or password."
                return render_template('login.html', error=error)

            session['username'] = admin['admin_name']
            return redirect(url_for('admin_view'))

        else:
            error = "No such User exists."
            return render_template('login.html', error=error)

    return render_template('login.html')


def logout():
    session.clear()
    return redirect(url_for('home'))


def user_home():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    
    user_count = get_user_count()
    donor_count = get_donor_count()
    hospital_count = get_hospital_count()

    user = get_user_by_username(username)
    is_donor = bool(user) and 'donor_list' in user

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
        return redirect('/userhome')

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
            return redirect(url_for('user_profile')) 
        else:
            flash("Current password is incorrect!", "error")

    return render_template('change_password.html')


def delete_account():
    if 'username' not in session:
        return redirect(url_for('login'))  

    if request.method == 'POST':
        username = session['username']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash("Passwords do not match!", "error")
            return redirect(request.url)

        user = get_user_by_username(username)

        if user and check_password_hash(user['pass'], password):  
            delete_user(username)
            session.clear() 
            flash("Sorry to see you go. Account deleted.", "success")
            return redirect(url_for('login')) 
        else:
            flash("Incorrect password!", "error")  

    return render_template('delete_account.html')


def trusted_hospitals():
    hospitals = get_trusted_hospitals()
    return render_template('trusted_hospitals.html', hospitals=hospitals)


def donation_view():
    if request.method == 'POST':
        username = session.get('username')
        if not username:
            return redirect(url_for('login')) 
        has_suffered = request.form['hasSuffered']
        has_disease = request.form['hasDisease']
        is_smoker = request.form['isSmoker']
        donation_date = request.form['donationDate']
        approver_hospital = request.form['approverHospital']

        if has_suffered == 'YES' or has_disease == 'YES' or is_smoker == 'YES':
            flash('Denied due to medical history', 'error')
            return redirect(url_for('donation_form'))

        if not is_trusted_hospital(approver_hospital):
            flash('Approval is not from a trusted hospital.', 'error')
            return redirect(url_for('donation_form'))

        if is_already_donor(username):
            flash('You are already a donor.', 'info')
            return redirect(url_for('user_home'))

        add_donor(username, donation_date, approver_hospital)
        flash('You have been added as a donor. Thank You', 'success')
        return redirect(url_for('user_home'))

    return render_template('donation_form.html')


def donor_list():
    donors = get_donor_list()
    return render_template("donor_list.html", donors=donors)


def request_blood():
    if request.method == 'POST':
        if 'username' in session:
            loggedInUsername = session['username']
        else:
            return "User not logged in."

        # Collect form data
        name = request.form['name']
        age = request.form['age']
        blood_type = request.form['blood_type']
        quantity = request.form['quantity']
        unit = request.form['unit']
        hospital = request.form['hospital']
        date_needed = request.form['date_needed']
        contact = request.form['contact']
        reason = request.form['reason']

        if not all([name, age, blood_type, quantity, unit, hospital, date_needed, contact, reason]):
            return "<script>alert('All fields are required.\nPlease fill them up with correct information.')</script>"

        insert_blood_request(loggedInUsername, name, age, blood_type, quantity, unit, hospital, date_needed, contact, reason)

        return redirect(url_for('user_home'))

    return render_template('request_blood.html')

def blood_requests():
    requests_data = get_all_blood_requests()
    return render_template('bloodrequests_list.html', requests=requests_data)


def campaigns_view():
    campaigns = get_campaigns()
    return render_template('campaigns.html', campaigns=campaigns)


def team_page():
    team_members = [
        {
            'name': 'Jannatul Ferdous',
            'role': 'Worked with Frontend',
            'image': 'nawrin.jpg',
            'github': 'https://github.com/'
        },
        {
            'name': 'Md Samsul Arefin',
            'role': 'Worked with Frontend',
            'image': 'samsul.jpg',
            'github': 'https://github.com/Crosshairs532'
        },
        {
            'name': 'Fardous Nayeem',
            'role': 'Worked with Backend',
            'image': 'nayeem.jpg',
            'github': 'https://github.com/X-Irrelevant-X'
        },
        {
            'name': 'Monowarul Islam',
            'role': 'Worked with Backend',
            'image': 'monowarul.jpg',
            'github': 'https://github.com/ShrabanMI'
        },
        {
            'name': 'Naser-Al-Noman',
            'role': 'Worked with Database',
            'image': 'naser.jpg',
            'github': 'https://github.com/Naser-Al-Noman'
        },
    ]
    return render_template('team.html', team=team_members)


#Admin Functions
def admin_view():
    if request.method == 'POST':
        username = request.form.get('username')
        delete_donor(username)
        return redirect(url_for('admin_view')) 

    donors = get_donor_list()
    return render_template('admin_view.html', donors=donors)
