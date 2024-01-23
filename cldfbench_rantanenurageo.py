import re
import copy
import logging
import pathlib
import warnings
import itertools
import collections

from clldutils.misc import slug
from clldutils.jsonlib import dump
from csvw.dsv import Dialect
from cldfbench import Dataset as BaseDataset, CLDFSpec

logging.getLogger("shapely.geos").setLevel(logging.WARNING)
warnings.simplefilter(action='ignore', category=FutureWarning)

URL = "https://zenodo.org/records/4784188/files/" \
      "Geographical%20database%20of%20the%20Uralic%20languages.zip?download=1"
PREFIX = 'Geographical database of the Uralic languages/Geospatial datasets/'
PATHS = {
    'Language distributions/Expert distributions/Language branches_no overlap/': [
        'Uralic_languages_traditional_OGUL.cpg',
        'Uralic_languages_traditional_OGUL.dbf',
        'Uralic_languages_traditional_OGUL.prj',
        'Uralic_languages_traditional_OGUL.sbn',
        'Uralic_languages_traditional_OGUL.sbx',
        'Uralic_languages_traditional_OGUL.shp',
        'Uralic_languages_traditional_OGUL.shp.xml',
        'Uralic_languages_traditional_OGUL.shx',
    ],
    'Language coordinates/': ['Uralic_coordinates.csv'],
}
# Harmonize dialect names across source files:
VARIETIES = {
    ("Erzya", "Western (Insar)"): "Western",
    ("Erzya", "North-Western (Alatyr)"): "North-Western",
    ("Erzya", "South-Eastern (Sura)"): "South-Eastern",
    ("Erzya", "Mixed (Shoksha)"): "Mixed",
    ("East Khanty", "Vakh-Vasjugan Khanty"): "Vakh-Vasyugan Khanty",
    ("Northern Selkup", "Bajixa"): "Baikha",
    ("Northern Selkup", "Upper-Tol'ka"): "Upper-Tolka",
    ("Northern Selkup", "Eloguj"): "Yelogui",
    ("Tomsk region Selkup", "Central"): "Central Selkup",
    ("Tomsk region Selkup", "Southern (Middle Ob')"): "Southern Selkup",
    ("Tomsk region Selkup", "Southern (?aja)"): "Southern Selkup",
    ("Tomsk region Selkup", "Ket'"): "Ket' Selkup",
    ("Hungarian", "Transylvanian Plain"): "Transylvanian plain",
}


def normalize(l, d):
    d = d or ''
    l = re.sub(r'\s+', ' ', l)
    d = re.sub(r'\s+', ' ', d)
    if d == l:
        d = ''
    d = d.replace(l, '').replace('dialects', '').replace('dialect', '').strip()
    d = VARIETIES.get((l, d), d)
    return l, d


def multi_polygon(f):
    if f['geometry']['type'] == 'Polygon':
        return copy.copy([f['geometry']['coordinates']])
    assert f['geometry']['type'] == 'MultiPolygon'
    return copy.copy(f['geometry']['coordinates'])


def shp2geojson(shp):
    import geopandas
    from fiona.crs import from_epsg
    from shapely.geometry import Polygon, shape

    # Re-project to EPSG 4326, aka WGS 84
    data = geopandas.read_file(str(shp))
    data_proj = data.copy()
    data_proj['geometry'] = data_proj['geometry'].to_crs(epsg=4326)
    data_proj.crs = from_epsg(4326)

    # Aggregate features per (language, dialect) pair:
    features = collections.OrderedDict()
    count = 0
    for feature in data_proj.__geo_interface__['features']:
        props = feature['properties']
        keys = [(props['Language'], None)]
        if props['Dialect']:
            keys.append((props['Language'], props['Dialect']))
        del props['Otherinfo']
        del props['Language']
        del props['Dialect']

        for key in keys:
            key = normalize(*key)
            if key in features:
                features[key]['geometry']['coordinates'].extend(multi_polygon(feature))
            else:
                count += 1
                features[key] = {
                    'id': count,
                    'type': 'Feature',
                    'properties': copy.copy(props),
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': multi_polygon(feature)
                    }
                }

    for (l, d), f in features.items():
        f['properties']['Language'] = l
        f['properties']['Dialect'] = d
        # Remove duplicate polygons:
        f['geometry']['coordinates'] = sorted(set(f['geometry']['coordinates']))

        # Fix polygons:
        mp = None
        for i, poly in enumerate(f['geometry']['coordinates']):
            rings = []
            for ring in poly:
                # Some linear rings are self-intersecting. We fix these by taking the 0-distance
                # buffer around the ring instead.
                p = Polygon(ring)
                if not p.is_valid:
                    p = p.buffer(0)
                    assert p.is_valid
                rings.append(p.__geo_interface__['coordinates'][0])
            p = shape(dict(type='Polygon', coordinates=rings))
            assert p.is_valid
            if mp is None:
                mp = shape(dict(type='MultiPolygon', coordinates=[rings]))
            else:
                mp = mp.union(p)
            assert mp.is_valid
        f['geometry'] = mp.__geo_interface__

    return features


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "rantanenurageo"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(dir=self.cldf_dir, module="Generic")

    def cmd_download(self, args):
        paths = [
            PREFIX + p for p in itertools.chain(*[[k + vv for vv in v] for k, v in PATHS.items()])]
        self.raw_dir.download_and_unpack(URL, *paths)

    def cmd_makecldf(self, args):
        from shapely.geometry import shape, Point

        args.writer.cldf.add_component(
            'LanguageTable',
            'Branch',
            'Language',
            'Dialect',
            {
                'name': 'Speaker_Area',
                'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#speakerArea',
            },
        )
        #
        # FIXME: replace areas.csv with MediaTable and speakerArea property!
        #
        args.writer.cldf.add_component('MediaTable')

        geojson = {
            'type': 'FeatureCollection',
            'properties': {
                'dc:description': 'Speaker areas of uralic language varieties in the traditional time period',
            },
            'features': []
        }

        langs = {
            normalize(r['Language'], r['Dialect']): r
            for r in self.etc_dir.read_csv('languages.csv', dicts=True)}
        gcodes = {r['ExactMatch']: r for r in langs.values() if r['ExactMatch']}
        polygons = {
            normalize(*k): v
            for k, v in shp2geojson(self.raw_dir / 'Uralic_languages_traditional_OGUL.shp').items()}
        kamas_mator = polygons['Kamas and Mator', '']
        polygons['Kamas', ''] = kamas_mator
        polygons['Mator', ''] = kamas_mator
        ul = self.raw_dir.read_csv(
            'Uralic_coordinates.csv',
            dialect=Dialect(skipRows=2, delimiter=';', encoding='cp1252'),
            dicts=True)

        def name(l, d):
            if not d:
                return l
            return '{} [{}]'.format(l, d)

        seen, lids = set(), set()
        for row in sorted(ul, key=lambda r: (r['Branch'], r['Language'])):
            #
            # Fix point location for North Karelian, see
            # https://github.com/cldf-datasets/rantanenurageo/issues/5
            #
            if row['Language variant/dialect'] == 'North Karelian':
                assert 65.16 < float(row['Latitude']) < 65.18
                row['Latitude'] = '65.27'

            l, d = normalize(row['Language'], row['Language variant/dialect'])
            if (l, d) not in langs:
                # If we cannot match by name, make sure we can match by exact Glottocode:
                assert row['Glottocode'] in gcodes
                lang = gcodes[row['Glottocode']]
                l, d = normalize(lang['Language'], lang['Dialect'])

            if ((l, d) in seen) and row['Glottocode'] in gcodes:
                lang = gcodes[row['Glottocode']]
                d = '{} [{}]'.format(d, row['Glottocode'])
            else:
                lang = langs[l, d]
                seen.add((l, d))
            cldf_lang = dict(
                ID=slug(name(l, d), lowercase=False),
                Name=name(l, d),
                Language=l,
                Dialect=d,
                Branch=row['Branch'],
                Latitude=row['Latitude'],
                Longitude=row['Longitude'],
                Glottocode=lang['ExactMatch'],
            )
            if cldf_lang['ID'] in lids:
                # See https://github.com/cldf-datasets/rantanenurageo/issues/4
                assert cldf_lang['ID'] == 'TomskregionSelkupSouthernSelkup'
                continue

            lids.add(cldf_lang['ID'])
            args.writer.objects['LanguageTable'].append(cldf_lang)
            if (l, d) in polygons:
                point = Point(float(row['Longitude']), float(row['Latitude']))
                assert point.within(shape(polygons[l, d]['geometry'])), '{} - {}'.format(l, d)
                geojson['features'].append(polygons[l, d])

        dump(geojson, self.cldf_dir / 'speaker_areas.geojson', indent=2)
        args.writer.objects['MediaTable'].append(dict(
            ID='rantanenurageo',
            Media_Type='application/geo+json',
            Download_URL='speaker_areas.geojson'))
