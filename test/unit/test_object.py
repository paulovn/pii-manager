

from text_anonymizer.tasks import AnonTask
from text_anonymizer import TextAnonymizer


TEST = ('El número de la tarjeta de crédito es 4273 9666 4581 5642',
        'El número de la tarjeta de crédito es <CREDIT_CARD>',)

def test10_constructor():
    obj = TextAnonymizer('es', None, AnonTask.CREDIT_CARD)
    assert obj.tasks[0][0] == AnonTask.CREDIT_CARD


def test20_info():
    obj = TextAnonymizer('es', None, AnonTask.CREDIT_CARD)
    exp = {AnonTask.CREDIT_CARD: "Credit card numbers for most international credit cards (recognize & validate)"}
    print(obj.tasks)
    got = {k[0]: k[2] for k in obj.tasks}
    assert exp == got


def test20_call():
    obj = TextAnonymizer('es', None, AnonTask.CREDIT_CARD)
    anon = obj(TEST[0])
    assert anon == TEST[1]

