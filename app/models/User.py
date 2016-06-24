""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()
    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database
    """
    def create_user(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        password = info['password']
        pw_hash = self.bcrypt.generate_password_hash(password)

        if not info['first_name']:
            errors.append('First Name cannot be blank!')
        elif len(info['first_name'])<2:
            errors.append('First Name must be at least 2 characters long')
        elif any(char.isdigit() for char in info['first_name']):
            errors.append('First Name must be letters only')

        if not info['last_name']:
            errors.append('Last Name cannot be blank!')
        elif len(info['last_name']) < 2:
            errors.append('Last Name must be at least 2 characters long')
        elif any(char.isdigit() for char in info['last_name']):
            errors.append('Last Name must be letters only')

        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')

        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['confirm_pw']:
            errors.append('Password and confirmation must match!')
        # If we hit errors, return them, else return True.
        if errors:
            return {"status": False, "errors": errors}
        else:
            # Code to insert user goes here...
            insert_query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at, updated_at) VALUES (:first_name, :last_name, :email, :pw_hash, NOW(), NOW())"
            data = { 'first_name': info['first_name'],
                     'last_name': info['last_name'],
                     'email': info['email'],
                     'pw_hash': pw_hash
                    }
            self.db.query_db(insert_query, data)

            # Then retrieve the last inserted user.
            get_user_query = "SELECT * FROM users ORDER BY user_id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return {"status": True, "user": users[0]}

    def login_user(self, info):
        password = info['password']
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': info['email']}
        user = self.db.query_db(user_query, user_data)
        if user:
            if self.bcrypt.check_password_hash(user[0]['pw_hash'], password):
                return user

        return False


