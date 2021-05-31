"""

"""
import shutil
import pathlib
import argparse
import webbrowser

from clldutils.clilib import PathType

from . import geojson


def register(parser):
    # Allow filtering by language-only, dialect-only, list of glottocodes
    parser.add_argument(
        '-o', '--output', type=PathType(must_exist=False, type='dir'), default=pathlib.Path('.'))
    parser.add_argument('--callback', default='parseGeojson', help=argparse.SUPPRESS)
    parser.add_argument('--branches', default=None, type=lambda s: s.split(','))


def run(args):
    outdir = args.output
    if not outdir.exists():
        outdir.mkdir()
    args.output = outdir / 'languages.js'
    geojson.run(args)
    shutil.copy(pathlib.Path(__file__).parent / 'index.html', outdir)
    webbrowser.open(str(outdir / 'index.html'))
