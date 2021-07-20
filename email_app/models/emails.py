from config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_FORMAT_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Email:
    def __init__( self, data ):
        self.id = data['id'],
        self.email = data['email']
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "Select * FROM email"
        results = connectToMySQL('email').query_db(query)
        users = []
        for user in results:
            users.append( cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO email (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW())"
        results = connectToMySQL('email').query_db(query, data)
        return results

    @classmethod
    def get_email_by_id(cls, data):
        query = "SELECT * FROM email WHERE id = %(id)s"
        results = connectToMySQL('email').query_db(query, data)
        return results

    @classmethod
    def email_not_in_db(cls, data):
        query = "SELECT * FROM email WHERE email = %(email)s;"
        results = connectToMySQL('email').query_db(query, data)
        return len(results) == 0

    @staticmethod
    def validate(user):
        is_valid = True
        if len(user) < 0:
            flash('No email submitted. Please enter and email address', 'email_address')
            is_valid = False
        if not EMAIL_FORMAT_REGEX.match(user['email']):
            flash('Invalid email address', 'email')
            is_valid = False
        if not Email.email_not_in_db(user):
            flash('A user with the email already exists', 'email')
            is_valid = False
        return is_valid