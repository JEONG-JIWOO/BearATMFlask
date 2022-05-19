from flask import Flask, request, session, jsonify
from datetime import timedelta
import bankapi
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)


@app.route('/insert_card', methods=['GET'])
def insert_card():
    session['card_number'] = request.form['card_number']
    if session['card_number'] is None:
        return "no card number", 400
    else:
        # you can add 'g.card_number' validation code on here if needed
        return 'Card added'


@app.route('/remove_card', methods=['POST'])
def remove_card():
    session['card_number'] = None
    session.clear()
    return 'Card removed'


@app.route('/enter_pin', methods=['GET'])
def enter_pin():
    pin_number = request.form['pin_number']
    if 'card_number' not in session:
        return "Insert card first", 400
    elif session['card_number'] is None:
        return "Insert card first", 400
    elif pin_number is None:
        return "No pin number ", 400
    elif not bankapi.validate_pin(session['card_number'], pin_number):
        return "Wrong Pin number", 401
    else:
        # save access token to session
        session['access_token'] = bankapi.login(session['card_number'], pin_number)
        return 'Authorized'


@app.route('/list_account', methods=['GET'])
def list_account():
    if 'access_token' not in session:
        return "Insert card first", 400
    else:
        session['account_list'] = bankapi.list_account(session['access_token'])
        return jsonify(session['account_list'])


@app.route('/select_account', methods=['GET'])
def select_account():
    account_id = request.form['account_id']
    if 'access_token' not in session:
        return "Insert card first", 400
    elif not account_id.isdigit():
        return "Wrong Account ID", 401
    elif 'account_list' not in session:
        session['account_list'] = bankapi.list_account(session['access_token'])

    account = bankapi.inquire(session['access_token'], account_id)
    if account is not None:
        session['selected_account'] = account
        return jsonify(account)
    else:
        return "account_ID not Found", 401


@app.route('/banking', methods=['GET'])
def banking():
    action = request.form['action']
    if 'access_token' not in session:
        return "Insert card first", 400
    elif 'selected_account' not in session:
        return "select account first", 400
    elif action == 'inquire':
        return bankapi.inquire(session['access_token'], session['selected_account']['id'])

    amount = request.form['amount']

    # before Banking, refresh Account Data
    session['selected_account'] = bankapi.inquire(session['access_token'], session['selected_account']['id'])
    if not amount.isdigit():
        return "Invalid amount", 400
    elif int(amount) < 0:
        return "Invalid amount", 400

    elif action == 'deposit':
        if bankapi.deposit(session['access_token'], session['selected_account']['id'], int(amount)):
            return "success"
        else:
            return "Fail", 403

    elif action == "withdraw":
        if session['selected_account']['balance'] < int(amount):
            return "not Enough Balance", 401
        elif bankapi.withdraw(session['access_token'], session['selected_account']['id'], int(amount)):
            return "success"
        else:
            return "Fail", 403

    else:
        return "Invalid Request", 400


@app.route('/')
def hello_world():
    return 'This is Bear Atm Backend Server'


if __name__ == '__main__':
    app.run()
