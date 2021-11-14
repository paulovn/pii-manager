'''
Spanish bank account numbers (CCC - código cuenta cliente)

Note: **NOT** IBAN numbers, those are country (& language) independent
'''

import re

from stdnum.es import ccc

from typing import Iterable

from text_anonymizer.tasks import AnonTask

# ----------------------------------------------------------------------------

# regex for a Código Cuenta Cliente, with optional spaces separating the pieces
_CCC_PATTERN = r'\d{4}\s?\d{4}\s?\d{2}\s?\d{10}'

# compiled regex
_REGEX_CCC = None


def init_bank_account():
    global _REGEX_CCC
    _REGEX_CCC = re.compile(_CCC_PATTERN, flags=re.X)


def get_bank_account(text: str) -> Iterable[str]:
    for item in _REGEX_CCC.findall(text):
        if ccc.is_valid(item):
            yield item


# ---------------------------------------------------------------------

ANONTASKS = [
    (AnonTask.BANK_ACCOUNT, init_bank_account, get_bank_account,
     "Spanish Bank Accounts (código cuenta cliente, 10-digit code, pre-IBAN), recognize & validate")
]
