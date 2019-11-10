from app import app
import random
import string

name = ''.join(random.choice(string.ascii_uppercase) for _ in range(12))
user = {"username":name, "dateOfBirth":"1981-01-02"}

def test_home():
    response = app.test_client().get('/')
    assert response.status_code == 200
    data = response.json
    assert data["message"] == "Happy Birthday!"

def test_add_user():
    response = app.test_client().post('/user', json=user)
    data = response.json
    assert response.status_code == 200
    assert data["username"] == user["username"]

def test_hello():
    response = app.test_client().get('/hello/{}'.format(user["username"]), json=user)
    data = response.json
    assert response.status_code == 200
    assert "Hello, {}!".format(user["username"]) in data["message"]