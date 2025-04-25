# BloodAid
Blood Aid is a rework of my old Blood Donation Service Project rebuilt in Flask and SQLite. Like the original project, users can view their profiles, post for blood donations with details, and view a donor list, sorted by blood group and area. There is also a campaigns feature where users can view ongoing blood donation campaigns and see its details.

New Encrytion features have been implemented using cryptography.fernet and werkzeug.security. Sensitive data, including user information, is encrypted while being stored and decrypted when displayed. Passwords are securely hashed and salted before being stored in the database. A key management system is also in place, where a dynamic encryption key is generated and stored in a .env file for handling encryption and decryption. To ensure data integrity, integrity checks are performed to prevent tampering.


# Be Aware
For New Users: Since the encryption key used for this version is randomly generated, it will not allow you to log in with previous credentials. You should create a new account and use those new credentials to log in. All other fields (like donors and blood requests) will show None until new data is added.

# Installation guide:

1. Clone the Repo and Unzip the Repo.
2. Create python environment inside the project folder.
    - open the terminal of IDE like VSCodoium or VSCode
    - python -m venv env
3. Activate the environment.
    - env\scripts\activate 
4. Move into the BA folder.
    - cd BA
5. Install the requirements.txt file.
    - pip install -r requirements.txt
6. Launch the project by running the app.py file
    - python app.py
