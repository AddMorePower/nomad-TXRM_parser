from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

import json
import os
import logging
import txrm2tiff as txrm
from nomad.config import config
from nomad.datamodel.metainfo.workflow import Workflow
from nomad.parsing.parser import MatchingParser

import nomad_txrm_parser.schema_packages.schema_package as txrm_schema

configuration = config.get_plugin_entry_point(
    'nomad_txrm_parser.parsers:parser_entry_point'
)


class NewParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        # logger.info('NewParser.parse', parameter=configuration.parameter)

        self.mainfile = mainfile
        self.archive = archive
        self.maindir = os.path.dirname(self.mainfile)
        self.mainfile = os.path.basename(self.mainfile)
        self.logger = logging.getLogger(__name__) if logger is None else logger

        try:
            self.txrm_file = txrm.open_txrm(mainfile)
        except Exception:
            self.logger.error('Error opening .txrm file')
            self.data = None
            return

        self.txrm_file.open()
        self.metadata = txrm.txrm_functions.get_image_info_dict(self.txrm_file.ole)

        self.sec_data = txrm_schema.TXRMOutput()
        archive.data = self.sec_data

        self.sec_data.angles = self.metadata['Angles']
        self.sec_data.camera_name = self.metadata['CameraName'][0]
        self.sec_data.current = self.metadata['Current'][0]
        self.sec_data.dates = self.metadata['Date']
        self.sec_data.energies = self.metadata['Energy']
        self.sec_data.exposure_times = self.metadata['ExpTimes']
        self.sec_data.horizontal_bin = self.metadata['HorizontalBin'][0]
        self.sec_data.vertical_bin = self.metadata['VerticalalBin'][0]
        self.sec_data.image_height = self.metadata['ImageHeight'][0]
        self.sec_data.image_width = self.metadata['ImageWidth'][0]
        self.sec_data.images_taken = self.metadata['ImagesTaken'][0]
        self.sec_data.ion_chamber_currents = self.metadata['IonChamberCurrent']
        self.sec_data.mosaic_fast_axis = self.metadata['MosaicFastAxis'][0]
        self.sec_data.mosaic_slow_axis = self.metadata['MosaicSlowAxis'][0]
        self.sec_data.mosaic_column = self.metadata['MosiacColumns'][0]
        self.sec_data.mosaic_rows = self.metadata['MosiacRows'][0]
        self.sec_data.mosaic_mode = self.metadata['MosiacMode'][0]
        self.sec_data.nb_images = self.metadata['NoOfImages'][0]
        self.sec_data.objective_name = self.metadata['ObjectiveName'][0]
        self.sec_data.optical_magnification = self.metadata['OpticalMagnification'][0]
        self.sec_data.pixel_size = self.metadata['PixelSize'][0]
        self.sec_data.temperature = self.metadata['Temperature'][0]
        self.sec_data.x_position = self.metadata['XPosition']
        self.sec_data.y_position = self.metadata['XrayMagnification']
        self.sec_data.z_position = self.metadata['YPosition']
        self.sec_data.xray_magnification = self.metadata['ZPosition']
        self.sec_data.zone_plate_name = self.metadata['ZonePlateName']

        try:
            with open('metadata.json', 'r') as md_file:
                md = json.load(md_file)
                self.sec_data.operator = md['Operator']
                self.sec_data.sample_type = md['Sample type']
                self.sec_data.sample_subtype = md['Sample Sub-Type']
                self.sec_data.sample_name = md['Sample name']
                self.sec_data.elements_thickness = md['Relevant elements and thickness']
                self.sec_data.xray_source = md['X-ray source']
                self.sec_data.resolution = md['Resolution']
                self.sec_data.contrast = md['Contrast']
                self.sec_data.project = md['Project']
                self.sec_data.microscope_name = md['Microscope name']
        except FileNotFoundError:
            pass
