from app.models import db, User, Transaction
from flask import Blueprint, request, jsonify, _request_ctx_stack, abort, json
import random
from functools import wraps


api = Blueprint('api', __name__, url_prefix='/api')

def authorize(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('API key')

        #Hardcoded API key for testing
        if api_key != "P9H6tqQmX7atj5snuHTGL6ru4Vqh6r":
            abort(401)
        return func(*args, **kwargs)

    return decorated_function

@api.route('/users', methods=['POST','GET'])
def api_users():
    if request.method == 'POST':
        if not request.json or not 'email' in request.json:
            abort(400)
        c = request.get_json()
        email = c['email']
        username = c['username']
        first_name = c['first_name']
        last_name = c['last_name']
        password = c['password']
        is_admin = c['is_admin']

        new_user = User(email=email, username=username, first_name=first_name, last_name=last_name,
                                password=password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User was created succesfully', "User": new_user.to_json(), 'status':'successful', 'status_code':200})
    else:
        users = User.query.all()
        if not users:
            return jsonify({'message': 'No users exist', 'status':'failed', 'status_code': 400})
        all_users = {'Users': [user.to_json() for user in users], 'status':'successful', 'status_code':200}

        return jsonify(all_users)

@api.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def api_user(id):
    if request.method == 'PUT':
        emp = User.query.get(id)
        c = request.get_json()
        if not c or not emp:
            abort(400)
        email = c['email']
        username = c['username']
        first_name = c['first_name']
        last_name = c['last_name']
        is_admin = c['is_admin']

        emp.email = email
        emp.username = username
        emp.first_name = first_name
        emp.last_name = last_name
        emp.is_admin = is_admin

        db.session.commit()

        return jsonify({'message': 'User was updated succesfully', "User": emp.to_json(), 'status':'successful', 'status_code':200})
    if request.method == 'GET':
        user = User.query.get(id)
        if not user:
            return jsonify({'message': 'User does not exist', 'status':'failed', 'status_code':400})

        return jsonify({"User": user.to_json(), 'status':'successful', 'status_code':200})

    if request.method == 'DELETE':
        user = User.query.get(id)
        if not user:
            return jsonify({'message': 'User does not exist', 'status':'failed', 'status_code':400})
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User was deleted succesfully', 'status':'successful', 'status_code':200})


@api.route('/airtime/send', methods=['POST'])
@authorize
def api_send_airtime():
    if not request.json:
        abort(400)

    c = request.get_json()
    username = c['username']
    r = c['recipients']
    transaction_ref = random.randint(1000000,10000000)

    total_amount = 0
    num_sent = 0

    for element in r:
        phone_number = element['phoneNumber']
        amo = element['amount'].split(" ")
        amount = amo[1]
        validated = validate_amount(int(amount))
        print ("amount {}".format(amount))
        print ("validate {}".format(validated))

        if validated:
            try:
                tr = Transaction(username=username, phone_number=phone_number, amount=amount,
                                 transaction_ref=transaction_ref)
                db.session.add(tr)
                db.session.commit()
                total_amount += int(amount)
                num_sent += 1
            except Exception as e:
                db.session.rollback()
                print("Exception :{}".format(e))
        else:
            pass


    trans = db.session.query(Transaction).filter(Transaction.transaction_ref == str(transaction_ref))
    all_trans = [t.to_json() for t in trans]
    resp = jsonify({'numSent': num_sent, 'totalAmount': total_amount, 'totalDiscount': 0,
                    'responses':all_trans , 'errorMessage': 'None'})
    print(resp)
    return resp

def validate_amount(amount):
    if (amount>=10 and amount<=10000):
        return True;
    else:
        return False;



