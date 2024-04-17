'''
db
database file, containing all the logic to interface with the sql database
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import *

from pathlib import Path

import hashlib
import secrets

# creates the database directory
Path("database") \
    .mkdir(exist_ok=True)

# "database/main.db" specifies the database file
# change it if you wish
# turn echo = True to display the sql output
engine = create_engine("sqlite:///database/main.db", echo=False)

# initializes the database
Base.metadata.create_all(engine)

#generate a random salt
def generate_salt():
    return secrets.token_hex(16)

#hash password
def hash_password(password, salt):
    salted_password = password.encode() + salt.encode()
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    return hashed_password

# inserts a user to the database
def insert_user(username: str, password: str):
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    with Session(engine) as session:
        user = User(username=username, password=hashed_password, salt=salt)
        session.add(user)
        session.commit()

# gets a user from the database
def get_user(username: str):
    with Session(engine) as session:
        return session.get(User, username)