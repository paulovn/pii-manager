'''
Test Spanish Bank Accounts
'''

from text_anonymizer.tasks import AnonTask
from text_anonymizer import TextAnonymizer


TEST = [
    # A valid bank account number
    ('Código cuenta cliente: 2085 8720 60 1902070563',
     'Código cuenta cliente: <BANK_ACCOUNT>'),
    # No spaces
    ('Código cuenta cliente: 20858720601902070563',
     'Código cuenta cliente: <BANK_ACCOUNT>'),
    # An invalid bank account number
    ('Código cuenta cliente: 2085 8720 44 1902070563',
     'Código cuenta cliente: 2085 8720 44 1902070563'),
]


def test10_bank_account():
    obj = TextAnonymizer('es', 'ES', AnonTask.BANK_ACCOUNT)
    for doc, exp in TEST:
        got = obj(doc)
        assert exp == got


def test20_bank_account_undefined():
    '''
    Test under another country (hence it will NOT be defined)
    '''
    obj = TextAnonymizer('es', 'FR', AnonTask.BANK_ACCOUNT)
    for doc, exp in TEST:
        got = obj(doc)
        assert doc == got
