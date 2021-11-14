
import importlib
from pathlib import Path

from typing import Dict, List, Tuple
from types import ModuleType

TASK_ANY = 'any'

# Name of the list holding anonymizer tasks
_LISTNAME = 'ANONTASKS'

# --------------------------------------------------------------------------


_LANG = Path(__file__).parents[1] / 'lang'


def gather_anontasks(pkg: ModuleType, path: str) -> List[Tuple]:
    antasks = {}
    modlist = (m.stem for m in Path(path).iterdir() if m.suffix == '.py')
    for mname in modlist:
        mod = importlib.import_module('.' + mname, pkg)
        tasks = getattr(mod, _LISTNAME, None)
        if tasks:
            antasks.update({t[0].name: t for t in tasks})
    return antasks


def import_processor(lang: str, country: str = None) -> Dict:
    if lang == TASK_ANY:
        name = TASK_ANY
        path = _LANG / TASK_ANY
    elif country is None:
        name = f'{lang}.{TASK_ANY}'
        path = _LANG / lang / TASK_ANY
    else:
        name = f'{lang}.{country}'
        path = _LANG / lang / country

    #mod = importlib.import_module('...lang.' + name, __name__)
    return gather_anontasks('text_anonymizer.lang.' + name, path)


def country_list(lang: str) -> List[str]:
    '''
    Return all countries for a given language
    '''
    p = _LANG / lang
    return [d.name for d in p.iterdir() if d.is_dir() and d != '__pycache__']


def language_list() -> List[str]:
    return [d.name for d in _LANG.iterdir() if d.is_dir()]


# --------------------------------------------------------------------------

_TASKS = None


def _gather_all_tasks():
    '''
    Build the list of all tasks
    '''
    global _TASKS

    _TASKS = {}
    for lang in language_list():
        if lang == TASK_ANY:
            _TASKS[lang] = import_processor(lang)
        else:
            _TASKS[lang] = {country: import_processor(lang, country)
                            for country in country_list(lang)}


def get_taskdict() -> Dict:
    '''
    Return the dicit holding all implemented anonymizer tasks
    '''
    global _TASKS
    if _TASKS is None:
        _gather_all_tasks()
    return _TASKS
