"""
Bank APIs

1. Validate pin

2. Login and return access token

3.

"""
import os

# dummy account data

accounts_list = [
    {"id": 123, "name": 'ac01', 'balance': 12331},
    {"id": 124, "name": 'ac02', 'balance': 2330},
    {"id": 125, "name": 'ac03', 'balance': 323300},
]


def validate_pin(card_number, pin_number):
    """
    :param card_number: str
    :param pin_number: str
    :return: True, False

    [TODO]
    check card & pin number matched
    """
    if card_number == "" or pin_number == "":
        return False
    return True


def login(card_number, pin_number):
    """
    :param card_number: str
    :param pin_number: str
    :return: access token

    [TODO]
    login to Bank Account and return access code
    """
    return os.urandom(12)


def list_account(access_token):
    """
    :param access_token:
    :return: dict of accounts

    [TODO]
    use access_token, get account list from bank and return as list
    """
    return accounts_list


def inquire(access_token, account_id):
    """
    :param account_id:
    :param access_token:
    :return: account_info

    [TODO]
    use access_token and account id, get account info from bank and return as dict
    """

    for x in accounts_list:
        if x['id'] == int(account_id):
            return x

    return None

def deposit(access_token, account_id, amount):
    """
    :param access_token:
    :param account_id:
    :param amount:
    :return:
    [TODO]
    use access_token and account id, do deposit
    """
    account = None
    for x in accounts_list:
        if x['id'] == int(account_id):
            account = x
            break

    account['balance'] += amount
    return True


def withdraw(access_token, account_id, amount):
    """
    :param access_token:
    :param account_id:
    :param amount:
    :return:
    """
    account = None
    for x in accounts_list:
        if x['id'] == int(account_id):
            account = x
            break

    if account['balance'] < amount:
        return False
    else:
        account['balance'] -= amount
        return True
