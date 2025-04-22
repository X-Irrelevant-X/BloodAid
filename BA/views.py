from flask import *
import sqlite3
from models import *
from werkzeug.security import generate_password_hash, check_password_hash



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
            return redirect('/user_web_view')
        else:
            error = "Invalid username or password"

    return render_template('login.html', error=error)
