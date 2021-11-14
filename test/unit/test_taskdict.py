

import text_anonymizer.helper as mod
from text_anonymizer.tasks import AnonTask
from text_anonymizer.helper import TASK_ANY

def test_lang_all():
    taskdict = mod.get_taskdict()
    assert len(taskdict) >= 2
    elem = taskdict[TASK_ANY][AnonTask.CREDIT_CARD.name]
    print("ELEM", elem)
    assert len(elem) == 4
    assert elem[0] == AnonTask.CREDIT_CARD


def test_lang_es():
    taskdict = mod.get_taskdict()
    assert 'es' in taskdict
