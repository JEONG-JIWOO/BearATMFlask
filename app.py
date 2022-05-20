"""
Bear Atm Main APP

jiwoo - jeong
"""
import os
from datetime import timedelta
from flask import Flask, request, session, jsonify
import bankapi

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)


@app.route('/insert_card', methods=['GET'])
def insert_card():
    """
    receive Card number and Save to session
    :card_number : str
    :return: 400(Wrong request)  , 200(Success)
    """
    session['card_number'] = request.form['card_number']
    if session['card_number'] is None:
        return "no card number", 400
    # you can add 'g.card_number' validation code on here if needed
    return 'Card added'


@app.route('/remove_card', methods=['POST'])
def remove_card():
    """
    remove Card number from session and close session
    :return: 200(Success)
    """
    session['card_number'] = None
    session.clear()
    return 'Card removed'


@app.route('/enter_pin', methods=['GET'])
def enter_pin():
    """
    receive pin number and Get auth token From Banking APi
    :pin_number : str
    :return: 400(Wrong request)  , 401(Wrong pin), 200(Success)
    """
    pin_number = request.form['pin_number']
    if 'card_number' not in session:
        return "Insert card first", 400
    if session['card_number'] is None:
        return "Insert card first", 400
    if pin_number is None:
        return "No pin number ", 400
    if not bankapi.validate_pin(session['card_number'], pin_number):
        return "Wrong Pin number", 401

    # save access token to session
    session['access_token'] = bankapi.login(session['card_number'], pin_number)
    return 'Authorized'


@app.route('/list_account', methods=['GET'])
def list_account():
    """
    return list of accounts
    :return: 400(Wrong request)  , 200(Success)
    """
    if 'access_token' not in session:
        return "Insert card first", 400

    session['account_list'] = bankapi.list_account(session['access_token'])
    return jsonify(session['account_list'])


@app.route('/select_account', methods=['GET'])
def select_account():
    """
    select account
    :account_id : int
    :return: 400(Wrong request) , 401(Wrong account ID), 200(Success)
    """
    account_id = request.form['account_id']
    if 'access_token' not in session:
        return "Insert card first", 400
    if not account_id.isdigit():
        return "Wrong Account ID", 401
    if 'account_list' not in session:
        session['account_list'] = bankapi.list_account(session['access_token'])

    account = bankapi.inquire(session['access_token'], account_id)
    if account is not None:
        session['selected_account'] = account
        return jsonify(account)

    return "account_ID not Found", 401


@app.route('/banking', methods=['GET'])
def banking():
    """
    Do Banking
    :action: type of Banking 'inquire','deposit','withdraw'
    :amount: amount of deposit & withdraw
    :return: 400(Wrong request)  401(Not Enough Balance) 403(Fail in Bank Account) 200(Success)
    """
    if 'access_token' not in session or 'selected_account' not in session:
        return "Insert card or select account first", 400

    action = request.form['action']
    if action == 'inquire':
        return bankapi.inquire(session['access_token'], session['selected_account']['id'])

    amount = request.form['amount']
    if not amount.isdigit() or int(amount) < 0:
        return "Invalid amount", 400

    # before Banking, refresh Account Data
    session['selected_account'] = bankapi.inquire(session['access_token'],
                                                  session['selected_account']['id'])

    result = None
    if action == 'deposit':
        result = bankapi.deposit(session['access_token'],
                                 session['selected_account']['id'], int(amount))
    elif action == "withdraw":
        if session['selected_account']['balance'] < int(amount):
            return "not Enough Balance", 401
        result = bankapi.withdraw(session['access_token'],
                                  session['selected_account']['id'], int(amount))

    if result:
        return "success"
    return "Fail", 403


@app.route('/')
def hello_world():
    """
    simple server check
    :return: 200
    """
    return 'This is Bear Atm Backend Server'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
