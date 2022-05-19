import unittest, json
import requests


host = "http://127.0.0.1:5000/"

card_number = "1234-2345"
pin_number = "1234"


class MyAtmTestCase01(unittest.TestCase):
    def test_00_server_status(self):
        self.assertEqual(requests.get(host).status_code, 200)

    def test_10_insert_card(self):
        session = requests.Session()
        self.assertEqual(session.get(host + '/insert_card', data={'card_number': card_number}).status_code, 200)
        self.assertEqual(session.post(host + '/remove_card').status_code, 200)
        # no card_number in request
        self.assertEqual(session.get(host + '/insert_card', data={'s': card_number}).status_code, 400)

    def test_20_enter_pin_valid(self):
        session = requests.Session()
        self.assertEqual(session.get(host + '/insert_card', data={'card_number': card_number}).status_code, 200)
        self.assertEqual(session.get(host + '/enter_pin', data={'pin_number': pin_number}).status_code, 200)
        return session

    def test_21_enter_pin_invalid(self):
        session = requests.Session()
        # enter pin before login
        self.assertEqual(session.get(host + '/enter_pin', data={'pin_number': pin_number}).status_code, 400)
        self.assertEqual(session.get(host + '/insert_card', data={'card_number': card_number}).status_code, 200)
        # no Pin Number
        self.assertEqual(session.get(host + '/enter_pin', data={'s': pin_number}).status_code, 400)
        # wrong Pin Number
        self.assertEqual(session.get(host + '/enter_pin', data={'pin_number': ''}).status_code, 401)

    def test_30_list_select_accounts_valid(self):
        session = self.test_20_enter_pin_valid()
        r1 = session.get(host + '/list_account')
        self.assertEqual(r1.status_code, 200)
        r2 = session.get(host + '/select_account', data={'account_id': json.loads(r1.text)[0]['id']})
        self.assertTrue(isinstance(json.loads(r2.text)['balance'], int))
        return session

    def test_31_list_select_accounts_invalid(self):
        session = self.test_20_enter_pin_valid()
        # account id is not int
        self.assertEqual(requests.get(host + '/select_account', data={'account_id': "asdf"}).status_code, 400)
        # no account id
        self.assertEqual(session.get(host + '/select_account', data={'account_id': ""}).status_code, 401)
        # there is no account
        with self.assertRaises(json.decoder.JSONDecodeError):
            json.loads(session.get(host + '/select_account', data={'account_id': "-1"}).text)

    def test_40_banking_valid(self):
        session = self.test_30_list_select_accounts_valid()
        self.assertEqual(session.get(host + '/banking', data={'action': "inquire"}).status_code, 200)
        self.assertEqual(session.get(host + '/banking', data={'action': "deposit", "amount": 0}).status_code, 200)
        self.assertEqual(session.get(host + '/banking', data={'action': "withdraw", "amount": 1}).status_code, 200)

    def test_41_banking_Invalid(self):
        # no login
        self.assertEqual(requests.get(host + '/banking', data={'action': "aaa"}).status_code, 400)

        # Invalid Parameter
        session = self.test_30_list_select_accounts_valid()
        self.assertEqual(session.get(host + '/banking', data={'action': "aaa"}).status_code, 400)
        self.assertEqual(session.get(host + '/banking', data={'action': "deposit", "amount": -1}).status_code, 400)
        self.assertEqual(session.get(host + '/banking', data={'action': "withdraw", "amount": -1}).status_code, 400)

        # Withdraw over balance
        self.assertEqual(session.get(host + '/banking',
                                     data={'action': "withdraw", "amount": 999999999999}).status_code, 401)


if __name__ == '__main__':
    unittest.main()
