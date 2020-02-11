from app import app
import numpy as np
from tabulate import tabulate
from users import *
from flask import jsonify
from models import Customer,Amount_atm
from connect import DbConnect
from collections import defaultdict

BRANCH='pune'

@app.route('/deposit/<amount>', methods=['POST'])
@token_required
def deposit(current_user,amount):
    db_connection = DbConnect()
    count=defaultdict(int)
    data = request.get_json()
    current_balance=db_connection.session.query(Customer.balance).filter(Customer.card_number == current_user.card_number).first()
    query=db_connection.session.query(Amount_atm.denom_100,Amount_atm.denom_200,Amount_atm.denom_500,Amount_atm.denom_2000,Amount_atm.balance).\
        filter(Amount_atm.branch_name == BRANCH).first()

    for i in data.keys():
        count[i]+=int(data[i])
    atm_amount=int(query.balance)
    atm_amount+=int(amount)
    balance=current_balance.balance
    balance+=int(amount)
    to_update=db_connection.session.query(Customer).filter(Customer.card_number == current_user.card_number)\
        .update({Customer.balance: balance},synchronize_session = False)
    number_2000=count['2000']+int(query.denom_2000)
    number_500 = count['500'] + int(query.denom_500)
    number_200 = count['200'] + int(query.denom_200)
    number_100 = count['100'] + int(query.denom_100)
    atm_update=db_connection.session.query(Amount_atm).filter(Amount_atm.branch_name == BRANCH)\
        .update({Amount_atm.balance: atm_amount,Amount_atm.denom_2000: number_2000,Amount_atm.denom_500: number_500,Amount_atm.denom_200: number_200,Amount_atm.denom_100: number_100}
                ,synchronize_session = False)
    db_connection.session.commit()
    db_connection.session.close()
    return "Transaction Completed"

@app.route('/withdraw/<amount>', methods=['POST'])
@token_required
def withdraw(current_user,amount):
    db_connection = DbConnect()
    query = db_connection.session.query(Amount_atm.denom_100, Amount_atm.denom_200, Amount_atm.denom_500,
                                        Amount_atm.denom_2000, Amount_atm.balance). \
        filter(Amount_atm.branch_name == BRANCH).first()
    atm_amount=int(query.balance)

    if(int(amount)>20000):
        return "Transaction amount exceeded 20,000 limit"
    elif(int(amount)<100):
        return "Transaction amount is less than 100"
    elif(int(amount)%100!=0):
        return "Enter multiples of 100"
    elif(int(amount)>atm_amount):
        return "ATM OUT OF SERVICE"
    denom_dict=defaultdict(int)
    count=defaultdict(int)
    amount=int(amount)
    amount_final=int(amount)
    notes = [2000, 500, 200, 100]
    current_balance = db_connection.session.query(Customer.balance).filter(
        Customer.card_number == current_user.card_number).first()
    count[2000]=int(query.denom_2000)
    count[500] = int(query.denom_500)
    count[200] = int(query.denom_200)
    count[100] = int(query.denom_100)
    for i in notes:
        denomination=amount/i
        if(denomination>=count[i]):
            denom_dict[i]+=denomination
            count[i]-=denomination
            amount-=(denomination*i)
        else:
            continue
    matrix=[]
    balance=current_balance.balance-amount_final
    atm_amount-=amount_final
    balance_update = db_connection.session.query(Customer).filter(
        Customer.card_number == current_user.card_number).update({Customer.balance: balance}, synchronize_session=False)
    number_2000 = int(query.denom_2000)-count[2000]
    number_500 = int(query.denom_500)-count[500]
    number_200 = int(query.denom_200)-count[200]
    number_100 = int(query.denom_100)-count[100]
    atm_update = db_connection.session.query(Amount_atm).filter(Amount_atm.branch_name == BRANCH) \
        .update({Amount_atm.balance: atm_amount, Amount_atm.denom_2000: number_2000, Amount_atm.denom_500: number_500,
                 Amount_atm.denom_200: number_200, Amount_atm.denom_100: number_100}
                , synchronize_session=False)
    db_connection.session.commit()
    db_connection.session.close()
    denom=list()
    number=list()
    for key in denom_dict.keys():
        denom.append(key)
        number.append(denom_dict[key])
        matrix = np.column_stack((denom, number))
    return str((tabulate(matrix, headers=["denomination", "number"])))








