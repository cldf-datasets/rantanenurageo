"""

"""
import json
import csv

from clldutils.jsonlib import dump
from clldutils.clilib import PathType

from cldfbench_rantanenurageo import Dataset

csv.field_size_limit(3000000)


def register(parser):
    # Allow filtering by language-only, dialect-only, list of glottocodes
    parser.add_argument('-o', '--output', type=PathType(must_exist=False), default=None)
    parser.add_argument('--callback', default=None)
    parser.add_argument('--branches', default=None, type=lambda s: s.split(','))


def run(args):
    res = dict(type='FeatureCollection', features=[])
    cldf = Dataset().cldf_reader()
    features = {r['Language_ID']: r['SpeakerArea'] for r in cldf['areas.csv']}

    def filter(l):
        res = True
        if args.branches:
            res = res and l['Branch'] in args.branches
        return res

    lids = [l['ID'] for l in cldf['LanguageTable'] if filter(l)]
    res['features'] = [f for lid, f in features.items() if lid in lids]
    if args.output:
        if args.callback:
            args.output.write_text('{}({});'.format(
                args.callback, json.dumps(res)), encoding='utf8')
        else:
            dump(res, args.output, indent=4)
    else:
        print(json.dumps(res, indent=4))
