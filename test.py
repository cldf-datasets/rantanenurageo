import sys
import csv

csv.field_size_limit(sys.maxsize)


def test_valid(cldf_dataset, cldf_logger, cldf_sqlite_database):
    assert cldf_dataset.validate(log=cldf_logger)
    assert cldf_sqlite_database.query('select count(*) from languagetable')[0][0] == 154
