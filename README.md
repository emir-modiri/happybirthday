# happybirthday

## make local test
`python3 -m venv tutorial-env`
`source tutorial-env/bin/activate`
`pip3 install -r requirements.txt`
`pytest test.py`
`curl -d '{"username":"emir", "dateOfBirth":"1981-01-02"}' -H "Content-Type: application/json" -X POST localhost:5000/user`
```
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    dateOfBirth TEXT NOT NULL
);
```