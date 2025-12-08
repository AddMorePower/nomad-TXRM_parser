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
import logging
import os

import txrm2tiff as txrm
from nomad.config import config
from nomad.parsing.parser import MatchingParser

import nomad_txrm_parser.schema_packages.schema_package as txrm_schema

configuration = config.get_plugin_entry_point(
    'nomad_txrm_parser.parsers:parser_entry_point'
)


class NewParser(MatchingParser):
    def typing_units(self):
        try:
            with open(f'{self.maindir}/metadata.json') as md_file:
                md = json.load(md_file)
                txrm_schema.TXRMOutput.angles.unit = md['angles_units']
                cycling = md['cycling_parameters']
                txrm_schema.Cycling.pulse_length.unit = cycling['pulse_length_units']
                txrm_schema.Cycling.base_temperature.unit = cycling[
                    'base_temperature_units'
                ]
                txrm_schema.Cycling.peak_temperature.unit = cycling[
                    'peak_temperature_units'
                ]
                txrm_schema.Cycling.base_voltage.unit = cycling['base_voltage_units']
                txrm_schema.Cycling.peak_voltage.unit = cycling['peak_voltage_units']
                txrm_schema.Cycling.resistance_at_room_temperature.unit = cycling[
                    'resistance_units'
                ]
        except FileNotFoundError:
            self.logger.error("The complementary 'metadata.json' file was not found ")

    def parse_metadata_file(self):
        try:
            with open(f'{self.maindir}/metadata.json') as md_file:
                md = json.load(md_file)
                self.sec_data.operator = md['operator']
                self.sec_data.sample_type = md['sample_type']
                self.sec_data.sample_subtype = md['sample_subtype']
                self.sec_data.sample_name = md['sample_name']
                self.sec_data.relevant_elements_and_thickness = md[
                    'relevant_elements_and_thickness'
                ]
                self.sec_data.experimental_technique = md['experimental_technique']
                self.sec_data.microscope_name = md['microscope_name']
                self.sec_data.xray_source = md['xray_source']
                self.sec_data.resolution = md['resolution']
                self.sec_data.contrast = md['contrast']
                self.sec_data.project = md['project']
                self.sec_data.angles = md['angles']
                self.sec_data.electrical_setup = md['electrical_setup']
                self.sec_data.oscilloscope = md['oscilloscope']
                self.sec_data.power_supply = md['power_supply']
                self.parse_processing(md['processing'])
                self.parse_cycling(md['cycling_parameters'])
        except FileNotFoundError:
            self.logger.error("The complementary 'metadata.json' file was not found ")

    def parse_processing(self, md):
        processing = self.sec_data.m_create(txrm_schema.Processing)
        processing.reconstruction = md['reconstruction']
        processing.reconstruction_software = md['reconstruction_software']
        processing.segmentation = md['segmentation']
        processing.segmentation_labels = md['segmentation_labels']

    def parse_cycling(self, md):
        cycling = self.sec_data.m_create(txrm_schema.Cycling)
        cycling.cycling = md['cycling']
        cycling.cycling_type = md['cycling_type']
        cycling.number_cycles = md['number_cycles']
        cycling.pulse_length = md['pulse_length']
        cycling.base_temperature = md['base_temperature']
        cycling.peak_temperature = md['peak_temperature']
        cycling.base_voltage = md['base_voltage']
        cycling.peak_voltage = md['peak_voltage']
        cycling.resistance_at_room_temperature = md['resistance_at_room_temperature']

    def parse_raw_txrm_file(self):
        raw_txrm_md = self.sec_data.m_create(txrm_schema.RawTxrmMetadata)
        raw_txrm_md.angles = self.metadata['Angles']
        raw_txrm_md.camera_name = self.metadata['CameraName'][0]
        raw_txrm_md.current = self.metadata['Current'][0]
        # The list of dates from the TXRM file contains strange data that
        # might look something like this:
        # 'bx', '"', 'd_', '?', '#P', '-P', '07/31/25 02:56:25'
        # Filtering out strange data based on the length of the string
        filter_length = 2
        trimmed_dates = [d for d in self.metadata['Date'] if len(d) > filter_length]
        raw_txrm_md.dates = trimmed_dates
        raw_txrm_md.energies = self.metadata['Energy']
        raw_txrm_md.exposure_times = self.metadata['ExpTimes']
        raw_txrm_md.horizontal_bin = self.metadata['HorizontalBin'][0]
        raw_txrm_md.vertical_bin = self.metadata['VerticalalBin'][0]
        raw_txrm_md.image_height = self.metadata['ImageHeight'][0]
        raw_txrm_md.image_width = self.metadata['ImageWidth'][0]
        raw_txrm_md.images_taken = self.metadata['ImagesTaken'][0]
        raw_txrm_md.ion_chamber_currents = self.metadata['IonChamberCurrent']
        raw_txrm_md.mosaic_fast_axis = self.metadata['MosaicFastAxis'][0]
        raw_txrm_md.mosaic_slow_axis = self.metadata['MosaicSlowAxis'][0]
        raw_txrm_md.mosaic_column = self.metadata['MosiacColumns'][0]
        raw_txrm_md.mosaic_rows = self.metadata['MosiacRows'][0]
        raw_txrm_md.mosaic_mode = self.metadata['MosiacMode'][0]
        raw_txrm_md.nb_images = self.metadata['NoOfImages'][0]
        raw_txrm_md.objective_name = self.metadata['ObjectiveName'][0]
        raw_txrm_md.optical_magnification = self.metadata['OpticalMagnification'][0]
        raw_txrm_md.pixel_size = self.metadata['PixelSize'][0]
        raw_txrm_md.temperature = self.metadata['Temperature'][0]
        raw_txrm_md.x_position = self.metadata['XPosition']
        raw_txrm_md.y_position = self.metadata['YPosition']
        raw_txrm_md.z_position = self.metadata['ZPosition']
        raw_txrm_md.xray_magnification = self.metadata['XrayMagnification']
        raw_txrm_md.zone_plate_name = self.metadata['ZonePlateName']

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

        self.typing_units()

        self.sec_data = txrm_schema.TXRMOutput()
        archive.data = self.sec_data

        self.parse_metadata_file()
        self.parse_raw_txrm_file()
