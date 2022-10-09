from flask import Flask, request, jsonify
from pymongo import MongoClient
import re, datetime
from datetime import date
from getenv import *
import logging

app = Flask(__name__)

#Variable for the database connection
CLIENT = MongoClient( 
    host="mongodb://"+MONGO_INITDB_HOST_NAME+":27017/", 
    username=MONGO_INITDB_ROOT_USERNAME, 
    password=MONGO_INITDB_ROOT_PASSWORD
    )

logging.getLogger().setLevel(logging.INFO)

#Class to define all exception message
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# Insert about database
def insert(USERNAME,BIRTHDAY):
    try:
        CLIENT["revolut"]["birthdays"].find({"name": USERNAME})[0]
        CLIENT["revolut"]["birthdays"].update_one({"name": USERNAME}, {"$set": {"name": USERNAME, "birthday": BIRTHDAY }})
        raise InvalidUsage("Username "+USERNAME+" updated!", status_code=201)

    except IndexError:
        CLIENT["revolut"]["birthdays"].insert_one({ "name": USERNAME, "birthday": BIRTHDAY })
        raise InvalidUsage("Username "+USERNAME+" registered!", status_code=200)


# Find the USERNAME
def find(USERNAME):
    try:
        GET_DATE = CLIENT["revolut"]["birthdays"].find({"name": USERNAME})[0]["birthday"]
        if datetime.datetime.strptime(GET_DATE, "%Y-%m-%d").strftime("%m-%d") == date.today().strftime("%m-%d"):
            raise InvalidUsage("Hello, "+USERNAME+ "! Happy birthday!", status_code=200)

        else:
            NEXT_BIRTHDAY = abs(datetime.datetime.strptime(GET_DATE, "%Y-%m-%d").replace(year=date.today().year) - datetime.datetime.strptime(date.today().strftime("%Y-%m-%d"), "%Y-%m-%d")).days
            raise InvalidUsage("Hello, "+USERNAME+ "! Your birthday is in "+str(NEXT_BIRTHDAY)+" day(s)", status_code=200)

    except IndexError:
        raise InvalidUsage("Username not found", status_code=404)

# Verify the rules for username
def check_username(USERNAME):
    if bool(re.search(r"\d", USERNAME)):
        raise InvalidUsage("Incorrect username, should be str without number", status_code=500)

# Verify the rules for date
def validate(BIRTHDAY):
    try:
        datetime.datetime.strptime(BIRTHDAY, "%Y-%m-%d")
        if BIRTHDAY == date.today().strftime("%Y-%m-%d"):
            raise InvalidUsage("Incorrect date, should be different to today", status_code=500)

    except ValueError:
        raise InvalidUsage("Incorrect date, should be YYYY-MM-DD", status_code=500)

# POST method to keep the usernam and birthday
@app.route("/hello/<string:USERNAME>", methods= ["POST","GET","PUT"])
def hello(USERNAME):
    check_username(USERNAME)
    if request.method == "POST" or request.method == "PUT":
        validate(request.get_json()["BIRTHDAY"])
        insert(USERNAME,request.get_json()["BIRTHDAY"])
        
    if request.method == "GET":
        find(USERNAME)