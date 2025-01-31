import logging

from nomad.datamodel import EntryArchive

from nomad_txrm_parser.parsers.parser import NewParser


def test_parse_file():
    parser = NewParser()
    archive = EntryArchive()
    parser.parse(
        'tests/data/04_REF_SA_b1_180s_3x-Despeckle-Ave.xrm',
        archive,
        logging.getLogger(),
    )

    assert archive.data.camera_name == 'X-ray'
