import sys
import csv

csv.field_size_limit(sys.maxsize)


def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)
