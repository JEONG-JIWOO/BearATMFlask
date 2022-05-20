"""
Unit test Module For app.py

"""


import unittest
import json
import requests


HOST= "http://127.0.0.1:5000"

CARD_NUMBER = "1234-2345"
PIN_NUMBER = "1234"


class MyAtmTestCase01(unittest.TestCase):
    """
    Total 8 Test of app.py
    """
    def test_00_server_status(self):
        """
        basic server connection test
        """
        self.assertEqual(requests.get(HOST).status_code, 200)

    def test_10_insert_card(self):
        """
        /insert_card Method test
        """
        session = requests.Session()
        self.assertEqual(session.get(HOST + '/insert_card',
                                     data={'card_number': CARD_NUMBER}).status_code, 200)
        self.assertEqual(session.post(HOST + '/remove_card').status_code, 200)
        # no CARD_NUMBER in request
        self.assertEqual(session.get(HOST + '/insert_card',
                                     data={'s': CARD_NUMBER}).status_code, 400)

    def test_20_enter_pin_valid(self):
        """
        /enter_pin Method test > Valid Requests
        """
        session = requests.Session()
        self.assertEqual(session.get(HOST + '/insert_card',
                                     data={'card_number': CARD_NUMBER}).status_code, 200)
        self.assertEqual(session.get(HOST + '/enter_pin',
                                     data={'pin_number': PIN_NUMBER}).status_code, 200)
        return session

    def test_21_enter_pin_invalid(self):
        """
        /enter_pin Method test > Invalid Requests
        """
        session = requests.Session()
        # enter pin before login
        self.assertEqual(session.get(HOST + '/enter_pin',
                                     data={'pin_number': PIN_NUMBER}).status_code, 400)
        self.assertEqual(session.get(HOST + '/insert_card',
                                     data={'card_number': CARD_NUMBER}).status_code, 200)
        # no Pin Number
        self.assertEqual(session.get(HOST + '/enter_pin',
                                     data={'s': PIN_NUMBER}).status_code, 400)
        # wrong Pin Number
        self.assertEqual(session.get(HOST + '/enter_pin',
                                     data={'pin_number': ''}).status_code, 401)

    def test_30_list_select_account_valid(self):
        """
        /list &select_account Method test > valid Requests
        """
        session = self.test_20_enter_pin_valid()
        response_01 = session.get(HOST + '/list_account')
        self.assertEqual(response_01.status_code, 200)
        response_02 = session.get(HOST + '/select_account',
                                  data={'account_id': json.loads(response_01.text)[0]['id']})
        self.assertTrue(isinstance(json.loads(response_02.text)['balance'], int))
        return session

    def test_31_list_select_account_invalid(self):
        """
        /list &select_account Method test > invalid Requests
        """
        session = self.test_20_enter_pin_valid()
        # account id is not int
        self.assertEqual(requests.get(HOST + '/select_account',
                                      data={'account_id': "asdf"}).status_code, 400)
        # no account id
        self.assertEqual(session.get(HOST + '/select_account',
                                     data={'account_id': ""}).status_code, 401)
        # there is no account
        with self.assertRaises(json.decoder.JSONDecodeError):
            json.loads(session.get(HOST + '/select_account',
                                   data={'account_id': "-1"}).text)

    def test_40_banking_valid(self):
        """
        /banking Method test > valid Requests
        """
        session = self.test_30_list_select_account_valid()
        self.assertEqual(session.get(HOST + '/banking',
                                     data={'action': "inquire"}).status_code, 200)
        self.assertEqual(session.get(HOST + '/banking',
                                     data={'action': "deposit", "amount": 0}).status_code, 200)
        self.assertEqual(session.get(HOST + '/banking',
                                     data={'action': "withdraw", "amount": 1}).status_code, 200)

    def test_41_banking_invalid(self):
        """
        /banking Method test > Invalid Requests
        """
        # no login
        self.assertEqual(requests.get(HOST + '/banking',
                                      data={'action': "aaa"}).status_code, 400)

        # Invalid Parameter
        session = self.test_30_list_select_account_valid()
        self.assertEqual(session.get(HOST + '/banking',
                                     data={'action': "aaa"}).status_code, 400)
        self.assertEqual(session.get(HOST + '/banking',
                                     data={'action': "deposit", "amount": -1}).status_code, 400)
        self.assertEqual(session.get(HOST + '/banking',
                                     data={'action': "withdraw", "amount": -1}).status_code, 400)
        self.assertEqual(session.get(HOST + '/banking',
                                     data={'action': "withdraw",
                                           "amount": "asdf"}).status_code, 400)

        # Withdraw over balance
        self.assertEqual(session.get(HOST + '/banking',
                                     data={'action': "withdraw",
                                           "amount": 999999999999}).status_code, 401)


if __name__ == '__main__':
    unittest.main()
