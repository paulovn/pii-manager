'''
Test bitcoin addresses
'''


from text_anonymizer.tasks import AnonTask
from text_anonymizer import TextAnonymizer


TEST = [
    # A valid bitcoin address
    ('BTC address: 1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW62i',
     'BTC address: <BITCOIN_ADDRESS>'),
    # An invalid bitcoin address
    ('BTC address: 1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW623',
     'BTC address: 1AGNa15ZQXAZUgFiqJ2i7Z2DPU2J6hW623')
]


def test10_credit_card():
    obj = TextAnonymizer('en', None, AnonTask.BITCOIN_ADDRESS)
    for doc, exp in TEST:
        got = obj(doc)
        assert exp == got
