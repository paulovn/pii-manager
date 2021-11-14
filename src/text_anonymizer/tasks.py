'''
Enumeration that contains all defined anonymization tasks

Order is significant, in the sense that, on an anonymization job, tasks coming
earlier in the enum will be tried first. Hence the more generic tasks (tasks
that might collide with more specific ones) should come last
'''

from enum import Enum, auto


class AnonTask(Enum):
    CREDIT_CARD = auto()
    BITCOIN_ADDRESS = auto()
    IP_ADDRESS = auto()
    EMAIL_ADDRESS = auto()
    AGE = auto()
    BIRTH_DATE = auto()
    DEATH_DATE = auto()
    NORP = auto()
    DISEASE = auto()
    BANK_ACCOUNT = auto()
    GOV_ID = auto()
    PHONE_NUMBER = auto()
    LICENSE_PLATE = auto()
    STREET_ADDRESS = auto()
