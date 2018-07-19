from flask import redirect, request, jsonify, url_for, json
import csv
import os
import requests

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_URL = "http://192.168.56.102"
from . import home

@home.route('/')
def homepage():

    return ("Home page")


@home.route('/sendairtime')
def send_airtime():
    file_path = os.path.join(BASE_DIR, 'assets/employee.csv')
    input_file = csv.DictReader(open(file_path))
    emp_list = []
    for row in input_file:
        emp = {}
        emp["phoneNumber"] = "+" + row["Phone-Number"]
        emp["amount"] = "KES " + row["Amount"]
        emp_list.append(emp)

    status = post_transaction(emp_list)
    print(status)

    return ("Send Airtime")


def post_transaction(emp_list):
    payload = {
        'username': 'jumo',
        'recipients': emp_list
    }

    headers = {"API key": "P9H6tqQmX7atj5snuHTGL6ru4Vqh6r", "Content-Type": 'application/json'}
    response = requests.post(url=BASE_URL+"/api/airtime/send", json=payload, headers=headers)
    status = response.status_code

    return status