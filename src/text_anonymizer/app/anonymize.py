'''
Command-line script to process text files
'''

import sys
import argparse
import gzip
import bz2
import lzma

from typing import List, Tuple, TextIO

from text_anonymizer import TextAnonymizer


def openfile(name: str, mode: str) -> TextIO:
    '''
    Open files, raw text or compressed (gzip, bzip2 or xz)
    '''
    if name.endswith('.gz'):
        return gzip.open(name, mode, encoding='utf-8')
    elif name.endswith('.bz2'):
        return bz2.open(name, mode, encoding='utf-8')
    elif name.endswith('.xz'):
        return lzma.open(name, mode, encoding='utf-8')
    else:
        return open(name, mode, encoding='utf-8')


def show_tasks(tasklist: List[Tuple]):
    print("\n. Installed tasks:")
    for task in tasklist:
        print(" ", task[0].name, "\n   ", task[2])


def process(args: argparse.Namespace):
    '''
    Do processing
    '''
    anon = TextAnonymizer(args.lang, args.country, tasks=args.tasks,
                          all_tasks=args.all_tasks, template=args.template)

    if args.show_tasks:
        show_tasks(anon.tasks)

    with openfile(args.infile, 'rt') as fin:
        with openfile(args.outfile, 'wt') as fout:
            for line in fin:
                fout.write(anon(line))

    if args.show_stats:
        print("\n. Statistics:")
        for k, v in anon.stats.items():
            print(f'  {k:20} :  {v:5}')


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Anonymize a document')

    g0 = parser.add_argument_group('Input/output paths')
    g0.add_argument('infile', help='source file')
    g0.add_argument('outfile', help='destination file')

    g1 = parser.add_argument_group('Language specification')
    g1.add_argument('--lang', help='document language', required=True)
    g1.add_argument('--country', nargs='+', help='countries to use')

    g2 = parser.add_argument_group('Task specification')
    g21 = g2.add_mutually_exclusive_group(required=True)
    g21.add_argument('--tasks', nargs='+', help='anonymization tasks')
    g21.add_argument('--all-tasks', action='store_true',
                     help='add all anonymization tasks available')

    g3 = parser.add_argument_group('Other')
    g3.add_argument('--show-stats', action='store_true',
                    help='Show statistics')
    g3.add_argument('--show-tasks', action='store_true',
                    help='Show defined tasks')
    g3.add_argument('--template',
                    help='substitution template')

    return parser.parse_args(args)


def main(args: List[str] = None):
    if args is None:
        args = sys.argv[1:]
    args = parse_args(args)
    process(args)


if __name__ == '__main__':
    main()
