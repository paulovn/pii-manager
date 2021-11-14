'''
Definition of the main anonymization object
'''

import re
from functools import partial
from collections import defaultdict
from itertools import chain

from .tasks import AnonTask
from .helper import get_taskdict, TASK_ANY, country_list

from typing import Iterable, Callable, Tuple, Union, Pattern, List


# --------------------------------------------------------------------------

TYPE_ANONTASK = Union[Callable, str]


def _anonymizer_regex(regex: Pattern, name: str, s: str) -> Tuple[str, int]:
    '''Substitute a string through a RegEx'''
    return regex.subn(name, s)


def _anonymizer_call(call: Callable, name: str, s: str) -> Tuple[str, int]:
    '''
    Substitute a string through a callable that detects suitable fragments
    '''
    n = -1
    for n, sub in enumerate(call(s)):
        s = s.replace(sub, name)
    return s, n+1


def anon_call(name: str, task_init: Callable, task_get: TYPE_ANONTASK):
    '''
    Return the proper anonymizer call for a task
    If necessary, also call the task initializer
    '''
    if task_init:
        task_init()
    # For regexes, wrap it with the regex call; for
    return partial(_anonymizer_regex, re.compile(task_get, flags=re.X), name) \
        if isinstance(task_get, str) else \
        partial(_anonymizer_call, task_get, name)


# --------------------------------------------------------------------------


def fetch_all_tasks(lang: str,
                    country: Iterable[str] = None) -> Iterable[Tuple]:
    '''
    Return all available anonymizer tasks for a given language & (optionally)
    country
    '''
    taskdict = get_taskdict()
    # Language-independent
    for task in taskdict[TASK_ANY].values():
        yield task
    # Country-independent
    langdict = taskdict.get(lang, {})
    for task in langdict.get(TASK_ANY, {}).values():
        yield task
    # Country-specific
    if country:
        if country[0] == 'all':
            country = country_list(lang)
        for c in country:
            for task in langdict.get(c, {}).values():
                yield task


def fetch_task(taskname: str, lang: str,
               country: Iterable[str] = None) -> Iterable[Tuple]:
    '''
    Return a specific task for a given language & country
    (find the most specific task available)
    '''
    found = 0
    taskdict = get_taskdict()
    if isinstance(taskname, AnonTask):
        taskname = taskname.name

    langdict = taskdict.get(lang, {})
    if langdict:
        # First try: language & country
        if country:
            for c in country:
                task = langdict.get(c, {}).get(taskname)
                if task:
                    found += 1
                    yield task
        # Second try: only language
        task = langdict.get(TASK_ANY, {}).get(taskname)
        if task:
            found += 1
            yield task
    # Third try: generic task
    task = taskdict[TASK_ANY].get(taskname)
    if task:
        found += 1
        yield task

    # We didn't find anything
    if not found:
        print(f'Warning: cannot find any anon task for {taskname}, {lang}, {country}')


# --------------------------------------------------------------------------


class TextAnonymizer:

    def __init__(self, lang: str, country: List[str] = None,
                 tasks: Iterable[AnonTask] = None,
                 all_tasks: bool = False, template: str = None):
        '''
        Initalize an anonymizer object, loading & initializing all specified
        anonymization tasks
        '''
        # Sanitize input
        self.lang = lang.lower()
        if isinstance(country, str):
            country = [country]
        self.country = [c.lower() for c in country] if country else None
        if template is None:
            template = '<{id}>'

        # Get the list of tasks we will use
        if all_tasks:
            tasklist = fetch_all_tasks(self.lang, self.country)
        else:
            if isinstance(tasks, AnonTask):
                tasks = [tasks]
            tasklist = (fetch_task(name, self.lang, self.country)
                        for name in tasks)
            tasklist = list(filter(None, chain.from_iterable(tasklist)))

        tasklist = list(tasklist)

        # Build an ordered array of tasks processors
        taskproc = ((t[0],
                     anon_call(template.format(id=t[0].name), *t[1:3]),
                     t[3]) for t in tasklist)
        self.tasks = sorted(taskproc, key=lambda e: e[0].value)

        self.stats = defaultdict(int)


    def __call__(self, doc: str) -> str:
        '''
        Process a document, calling all defined anonymizers
        '''
        self.stats['calls'] += 1
        for task_id, task_proc, _ in self.tasks:
            doc, n = task_proc(doc)
            self.stats[task_id.name] += n
        return doc
