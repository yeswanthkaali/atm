from app import app
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from functools import wraps
from flask import request
from flask import jsonify,abort,make_response
from connect import DbConnect
from models import Customer



# token required to access all the operations



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        db_connection = DbConnect()
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db_connection.session.query(Customer.public_id,Customer.pin,Customer.card_number,Customer.admin).filter(Customer.public_id == data['public_id']).first()
            db_connection.session.close()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# posting a new user only by admin

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    db_connection = DbConnect()
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['pin'], method='sha256')

    new_user = Customer(public_id=str(uuid.uuid4()), card_number=data['card_number'], pin=hashed_password,admin= True,
                        balance=data['balance'])
    db_connection.session.add(new_user)
    db_connection.session.commit()
    db_connection.session.close()

    return jsonify({'message' : 'New user created!'})


@app.route('/login')
def login():
    auth = request.authorization
    db_connection = DbConnect()

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = db_connection.session.query(Customer.admin,Customer.card_number,Customer.pin,Customer.public_id).filter(Customer.card_number==auth.username).first()
    db_connection.session.close()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.pin, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=15)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})