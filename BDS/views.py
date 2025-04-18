from flask import render_template
from models import get_user_count, get_donor_count, get_hospital_count

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
