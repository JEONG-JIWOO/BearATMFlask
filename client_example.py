import requests ,json

if __name__ == '__main__':
    host = "http://127.0.0.1:5000/"
    session = requests.Session()

    # 1. Login
    card_number = input("enter Card :  ")
    if session.get(host + '/insert_card', data={'card_number': card_number}).status_code == 200:
        pin_number = input("enter Pin Number :  ")
        if session.get(host + '/enter_pin', data={'pin_number': card_number}).status_code == 200:
            print('login success! \n -----------------')

    # 2. Select Account
    account_list = json.loads(session.get(host + '/list_account').text)
    cnt = 0
    for account in account_list:
        print("[%d], %s %s"%(cnt, account['name'], account['balance']))
        cnt +=1

    index = int(input("select account :  "))
    aid = account_list[index]['id']
    if session.get(host + '/select_account', data={'account_id': aid}).status_code == 200:
        print("account selected \n %s : %s"%(account_list[index]['name'], account_list[index]['balance']))

    # 3. Banking
    while True:
        action = input("---------------- \n select action inquire, deposit , withdraw, break or i,d,w,b :  ").lower()

        if action == 'inquire' or action == 'i':
            r = json.loads(session.get(host + '/banking', data={'action': 'inquire'}).text)
            print(" %s : %s" % (r['name'], r['balance']))

        elif action == 'deposit' or action == 'd':
            amount = int(input("enter amount :  "))
            r = session.get(host + '/banking', data={'action': 'deposit','amount': amount})
            if r.status_code == 200:
                print("success")
            else :
                print("fail",r.text)

        elif action == 'withdraw' or action == 'w':
            amount = int(input("enter amount :  "))
            r = session.get(host + '/banking', data={'action': 'withdraw', 'amount': amount})
            if r.status_code == 200:
                print("success")
            else:
                print("fail", r.text)

        elif action == 'break' or action == 'b':
            session.post(host + '/remove_card')
            print("exit banking")
            break