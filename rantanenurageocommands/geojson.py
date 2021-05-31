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


def run(args):
    res = dict(type='FeatureCollection', features=[])
    cldf = Dataset().cldf_reader()
    features = {r['Language_ID']: r['SpeakerArea'] for r in cldf['areas.csv']}
    #for l in cldf.objects('LanguageTable'):
    res['features'] = list(features.values())
    if args.output:
        dump(res, args.output, indent=4)
    else:
        print(json.dumps(res, indent=4))
