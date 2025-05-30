from flask import Flask
from views import *

app = Flask(__name__)
app.secret_key = '2N3a3Y4e1e0M91@f2a1rd3o0u1s1a4S7K2*'

app.add_url_rule('/', view_func=home, endpoint='home')

app.add_url_rule('/register', view_func=register, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=logout, endpoint='logout')
app.add_url_rule('/userhome', view_func=user_home, endpoint='user_home')
app.add_url_rule('/user_profile', view_func=user_profile)

app.add_url_rule('/remove_donor', 'remove_donor_view', remove_donor_view, methods=['POST'])
app.add_url_rule('/change_password', 'change_password', change_password, methods=['GET', 'POST'])
app.add_url_rule('/delete_account', 'delete_account', delete_account, methods=['GET', 'POST'])
app.add_url_rule('/report_user', view_func=report_user, methods=['GET', 'POST'])

app.add_url_rule('/donation', 'donation_form', donation_view, methods=['GET', 'POST'])
app.add_url_rule('/donor_list', 'donor_list', donor_list)
app.add_url_rule('/trusted_hospitals', 'trusted_hospitals', trusted_hospitals)
app.add_url_rule('/request_blood', 'request_blood', request_blood, methods=['GET', 'POST'])
app.add_url_rule('/blood_requests', 'blood_requests', blood_requests)
app.add_url_rule('/campaigns', 'campaigns',view_func=campaigns_view)
app.add_url_rule('/team', 'team', view_func=team_page)

#Admin Routes
app.add_url_rule('/admin/view', 'admin_view', admin_view)
app.add_url_rule('/admin/delete_user', 'delete_user', delete_user_view, methods=['POST'])
app.add_url_rule('/admin/donors','admin_donors', view_func=admin_view_donors)
app.add_url_rule('/admin/delete_donor', view_func=delete_donor, methods=['POST'])

app.add_url_rule('/admin/requests', 'admin_requests', view_func=admin_requests)
app.add_url_rule('/admin/reports', 'admin_reports', admin_reports)

app.add_url_rule('/admin/campaigns', 'admin_campaigns', admin_campaigns, methods=['GET', 'POST'])
app.add_url_rule('/admin/delete_campaign', 'delete_campaign', delete_campaign_view, methods=['POST'])

app.add_url_rule('/admin/hospitals', 'admin_hospitals', admin_hospitals, methods=['GET', 'POST'])
app.add_url_rule('/admin/delete_hospital', view_func=delete_hospital, methods=['POST'])

