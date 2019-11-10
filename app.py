from flask import Flask, request, jsonify
from flask_api import status
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime, timedelta
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    dateOfBirth = db.Column(db.String(10))

    def __init__(self, username, dateOfBirth):
        self.username = username
        self.dateOfBirth = dateOfBirth
    
    def json(self):
        return {"username": self.username, "dateOfBirth": self.dateOfBirth}


class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'dateOfBirth')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

def until_birthday(original_date, now):
    delta1 = datetime(now.year, original_date.month, original_date.day)
    delta2 = datetime(now.year+1, original_date.month, original_date.day)
    days = (max(delta1, delta2) - now).days
    if days > 365:
        days = days - 365
    return days

# endpoint to home
@app.route("/", methods=["GET"])
def home():
    content = {"message":"Happy Birthday!"}
    return content, status.HTTP_200_OK

# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    try:
        username = request.json['username']
    except ValueError:
        content = {'error': 'username is empty!'}
        return jsonify(content), status.HTTP_400_BAD_REQUEST
    
    try:
        dateOfBirth = datetime.strptime(request.json['dateOfBirth'], "%Y-%m-%d")
    except ValueError:
        content = {'error': 'Incorrect data format, should be YYYY-MM-DD!'}
        return jsonify(content), status.HTTP_400_BAD_REQUEST

    if datetime.now() < dateOfBirth:
        content = {'error': 'date is not acceptable!'}
        return jsonify(content), status.HTTP_400_BAD_REQUEST

    if not username.isalpha():
        content = {'error': 'username filed must contain alphabe!'}
        return jsonify(content), status.HTTP_400_BAD_REQUEST

    new_user = User(username, dateOfBirth)
    try:
        db.session.add(new_user)
        db.session.commit()
    except ValueError:
        content = {'error': 'something goes wrong try it again!'}
        return jsonify(content), status.HTTP_400_BAD_REQUEST

    return new_user.json(), status.HTTP_200_OK

# endpoint to get user detail and say happybirthday
@app.route("/hello/<username>", methods=["GET"])
def hello(username):
    user = User.query.filter(User.username == username).first()

    if not user:
        content = {'error': 'username not found!'}
        return jsonify(content), status.HTTP_404_NOT_FOUND

    message = "Hello, {}! Happy Birthday!".format(user.username)
    remain_days = until_birthday(datetime.strptime(user.dateOfBirth, "%Y-%m-%d %H:%M:%S"), datetime.now())
    if remain_days > 0:
        message = "Hello, {}! Your Birthday is in {} day(s)!".format(user.username, remain_days)

    content = {"message": message}

    return content, status.HTTP_200_OK

# endpoint to update user
@app.route("/user/<username>", methods=["GET"])
def user_get(username):
    user = User.query.filter(User.username == username).first()

    if not user:
        content = {'error': 'username not found!'}
        return jsonify(content), status.HTTP_404_NOT_FOUND

    return user.json(), status.HTTP_200_OK

# endpoint to update user
@app.route("/user/<username>", methods=["PUT"])
def user_update(username):
    user = User.query.filter(User.username == username).first()

    if not user:
        content = {'error': 'username not found!'}
        return jsonify(content), status.HTTP_404_NOT_FOUND

    username = request.json['username']
    try:
        dateOfBirth = datetime.strptime(request.json['dateOfBirth'], "%Y-%m-%d")
    except ValueError:
        content = {'error': 'Incorrect data format, should be YYYY-MM-DD!'}
        return jsonify(content), status.HTTP_400_BAD_REQUEST

    if datetime.now() < dateOfBirth:
        content = {'error': 'date is not acceptable!'}
        return jsonify(content), status.HTTP_400_BAD_REQUEST

    if not username.isalpha():
        content = {'error': 'username filed must contain alphabe!'}
        return jsonify(content), status.HTTP_400_BAD_REQUEST

    user.dateOfBirth = dateOfBirth
    user.username = username

    db.session.commit()
    return '', status.HTTP_204_NO_CONTENT

if __name__ == '__main__':
    app.run(debug=True)