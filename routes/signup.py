from flask import Blueprint, request, jsonify
import helpers
from database_models import User
from database import db_session

signup_api = Blueprint('signup_api', __name__)


# NEW USER API
@signup_api.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()
    if 'username' not in data:
        raise ValueError("username is required")
    username = data['username']
    if 'password' not in data:
        raise ValueError("password is required")
    password = data['password']
    if 'email' not in data:
        raise ValueError("email is required")
    email = data['email']

    # check for valid data
    message = dict(username=username, email=email)
    success = True

    if not helpers.valid_username(str(username)):
        message['error_username'] = "Username is not valid"
        success = False
    if helpers.user_by_name(username) is not None:
        message['error_username'] = "Username is taken"
        success = False
    if not helpers.valid_password(password):
        message['error_password'] = "Password is not valid"
        success = False
    if not helpers.valid_email(email):
        message['error_email'] = "Email is not valid"
        success = False
    if helpers.user_by_email(str(email)) is not None:
        message['error_email'] = "Email already in use"
    if success is False:
        message['success'] = False
        return jsonify(message)

    # hash the password for db storage
    pw_hash = helpers.make_pw_hash(username, password)
    # create new user object with hashed password
    new_user = User(username, email, pw_hash)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    # return user JSON and status code
    return jsonify(user=new_user.serialize), 200
