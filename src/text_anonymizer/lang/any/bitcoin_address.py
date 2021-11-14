'''
Find valid bitcoin addresses
1. Obtain candidates, by using a generic regex expression
2. Validate candidates by
    - using a more exact regex
    - validating the number through the Luhn algorithm
'''

import re

from stdnum import bitcoin

from typing import Iterable

from text_anonymizer.tasks import AnonTask

# ----------------------------------------------------------------------------

# regex for the three types of bitcoin addresses
_BITCOIN_PATTERN = (r'( [13] [' + bitcoin._base58_alphabet + ']{25,34}' +
                    '| bc1 [' + bitcoin._bech32_alphabet + ']{8,87})')

_REGEX_BITCOIN = None


def init_bitcoin():
    global _REGEX_BITCOIN
    _REGEX_BITCOIN = re.compile(_BITCOIN_PATTERN, flags=re.X)


def get_bitcoin(text: str) -> Iterable[str]:
    '''
    Bitcoin addresses
    '''
    # Find candidates
    possible_bitcoin = _REGEX_BITCOIN.findall(text)

    # Validate candidates
    for ba in possible_bitcoin:
        if bitcoin.is_valid(ba):
            yield ba


# ---------------------------------------------------------------------

ANONTASKS = [
    (AnonTask.BITCOIN_ADDRESS, init_bitcoin, get_bitcoin,
     "Bitcoin addresses (P2PKH, P2SH and Bech32), recognize & validate")
]
