'''
Find valid credit card numbers:
1. Obtain candidates, by using a generic regex expression
2. Validate candidates by
    - using a more exact regex
    - validating the number through the Luhn algorithm
'''

import re

from typing import Iterable

from stdnum import luhn

from text_anonymizer.tasks import AnonTask


# ----------------------------------------------------------------------------

# regex for credit card type
# https://www.regular-expressions.info/creditcard.html
_CREDIT_PATTERN = r"""4[0-9]{12}(?:[0-9]{3})? |
                      (?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12} |
                      3[47][0-9]{13} |
                      3(?:0[0-5]|[68][0-9])[0-9]{11} |
                      6(?:011|5[0-9]{2})[0-9]{12} |
                      (?:2131|1800|35\d{3})\d{11}"""


_REGEX_CREDIT_CARD = None


def init_credit_card():
    global _REGEX_CREDIT_CARD
    _REGEX_CREDIT_CARD = re.compile(_CREDIT_PATTERN, flags=re.VERBOSE)


def get_credit_card(text: str) -> Iterable[str]:
    '''
    Credit card numbers
    '''
    # Find candidates
    possible_credit_card = re.findall(r"\b \d (?:\d[ -]?){14} \d \b",
                                      text, flags=re.X)

    # Validate candidates
    for cc in possible_credit_card:
        # strip spaces and dashes
        strip_cc = re.sub(r"[ -]+", "", cc)
        # validate the credit card number
        if re.fullmatch(_REGEX_CREDIT_CARD, strip_cc) and luhn.is_valid(strip_cc):
            yield cc


# ---------------------------------------------------------------------

ANONTASKS = [
    (AnonTask.CREDIT_CARD, init_credit_card, get_credit_card,
     "Credit card numbers for most international credit cards (recognize & validate)")
]
