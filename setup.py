from setuptools import setup


setup(
    name='cldfbench_rantanenurageo',
    py_modules=['cldfbench_rantanenurageo'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'rantanenurageo=cldfbench_rantanenurageo:Dataset',
        ],
        'cldfbench.commands': [
            'rantanenurageo=rantanenurageocommands',
        ],
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'geo': [
            'geopandas',
            'fiona',
            'shapely',
        ],
        'test': [
            'pytest-cldf',
        ],
    },
)
