'''
Find valid credit card numbers:
1. Obtain candidates, by using a generic regex expression
2. Validate candidates by
    - using a more exact regex
    - validating the number through the Luhn algorithm
'''

import re

from stdnum import luhn

from pii_manager import PiiEnum, PiiEntity
from pii_manager.helper import BasePiiTask


# ----------------------------------------------------------------------------

# regex for credit card type
# https://www.regular-expressions.info/creditcard.html
_TOY_PATTERN = r"""ABCD [\d-]5"""



# ---------------------------------------------------------------------

PII_TASKS = [(PiiEnum.DISEASE, _TOY_PATTERN, "a toy example")]
