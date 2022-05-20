"""
Eample Code of Bear ATM client
"""
import json
import requests

if __name__ == '__main__':
    HOST = "http://127.0.0.1:5000/"
    session = requests.Session()

    # 1. Login
    card_number = input("enter Card :  ")
    if session.get(HOST + '/insert_card', data={'card_number': card_number}).status_code == 200:
        pin_number = input("enter Pin Number :  ")
        if session.get(HOST + '/enter_pin', data={'pin_number': card_number}).status_code == 200:
            print('login success! \n -----------------')

    # 2. Select Account
    account_list = json.loads(session.get(HOST + '/list_account').text)
    CNT = 0
    for account in account_list:
        print(f"{CNT}, {account['name']} {account['balance']}")
        CNT += 1

    index = int(input("select account :  "))
    aid = account_list[index]['id']
    if session.get(HOST + '/select_account', data={'account_id': aid}).status_code == 200:
        print(f"select \n {account_list[index]['name']} : {account_list[index]['balance']}")

    # 3. Banking
    while True:
        action = input("---------------- \n select action inquire, deposit ,"
                       " withdraw, break or i,d,w,b :  ").lower()

        if action in ('inquire', 'i'):
            r = json.loads(session.get(HOST + '/banking', data={'action': 'inquire'}).text)
            print(f" {r['name']} : { r['balance']}")

        elif action in ('deposit' ,'d'):
            amount = int(input("enter amount :  "))
            r = session.get(HOST + '/banking', data={'action': 'deposit','amount': amount})
            if r.status_code == 200:
                print("success")
            else :
                print("fail",r.text)

        elif action in ('withdraw' ,'w'):
            amount = int(input("enter amount :  "))
            r = session.get(HOST + '/banking', data={'action': 'withdraw', 'amount': amount})
            if r.status_code == 200:
                print("success")
            else:
                print("fail", r.text)

        elif action in  ('break', 'b'):
            session.post(HOST + '/remove_card')
            print("exit banking")
            break
