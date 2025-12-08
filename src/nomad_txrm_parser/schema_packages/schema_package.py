# from typing import (
#     TYPE_CHECKING,
# )

# if TYPE_CHECKING:
#     from nomad.datamodel.datamodel import (
#         EntryArchive,
#     )
#     from structlog.stdlib import (
#         BoundLogger,
#     )

from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.metainfo import MSection, Quantity, SchemaPackage, SubSection

configuration = config.get_plugin_entry_point(
    'nomad_txrm_parser.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class RawTxrmMetadata(MSection):
    angles = Quantity(type=float, shape=['*'])
    camera_name = Quantity(type=str)
    current = Quantity(type=float, shape=[])
    dates = Quantity(type=str, shape=['*'])
    energies = Quantity(type=float, shape=['*'])
    exposure_times = Quantity(type=float, shape=['*'])
    horizontal_bin = Quantity(type=int, shape=[])
    vertical_bin = Quantity(type=int, shape=[])
    image_height = Quantity(type=int, shape=[])
    image_width = Quantity(type=int, shape=[])
    images_taken = Quantity(type=int, shape=[])
    ion_chamber_currents = Quantity(type=float, shape=['*'])
    mosaic_fast_axis = Quantity(type=int, shape=[])
    mosaic_slow_axis = Quantity(type=int, shape=[])
    mosaic_column = Quantity(type=int, shape=[])
    mosaic_rows = Quantity(type=int, shape=[])
    mosaic_mode = Quantity(type=int, shape=[])
    nb_images = Quantity(type=int, shape=[])
    objective_name = Quantity(type=str)
    optical_magnification = Quantity(type=float, shape=[])
    pixel_size = Quantity(type=float, shape=[])
    temperature = Quantity(type=float, shape=[])
    x_position = Quantity(type=float, shape=['*'])
    y_position = Quantity(type=float, shape=['*'])
    z_position = Quantity(type=float, shape=['*'])
    xray_magnification = Quantity(type=float, shape=['*'])
    zone_plate_name = Quantity(type=str, shape=['*'])


class Processing(MSection):
    reconstruction = Quantity(type=bool)
    reconstruction_software = Quantity(type=str)
    segmentation = Quantity(type=bool)
    segmentation_labels = Quantity(type=str)


class Cycling(MSection):
    cycling = Quantity(type=bool)
    cycling_type = Quantity(type=str)
    number_cycles = Quantity(type=int)
    pulse_length = Quantity(type=float)
    base_temperature = Quantity(type=float, unit='')
    peak_temperature = Quantity(type=float, unit='')
    base_voltage = Quantity(type=float, unit='')
    peak_voltage = Quantity(type=float, unit='')
    resistance_at_room_temperature = Quantity(type=float, unit='')


class TXRMOutput(Schema):
    operator = Quantity(type=str)
    sample_type = Quantity(type=str)
    sample_subtype = Quantity(type=str)
    sample_name = Quantity(type=str)
    relevant_elements_and_thickness = Quantity(type=str)
    experimental_technique = Quantity(type=str)
    microscope_name = Quantity(type=str)
    xray_source = Quantity(type=str)
    resolution = Quantity(type=str)
    contrast = Quantity(type=str)
    project = Quantity(type=str)
    angles = Quantity(type=float, unit='')
    electrical_setup = Quantity(type=str)
    oscilloscope = Quantity(type=str)
    power_supply = Quantity(type=str)
    raw_txrm_metadata = SubSection(sub_section=RawTxrmMetadata.m_def, repeats=False)
    processing = SubSection(sub_section=Processing.m_def, repeats=False)
    cycling = SubSection(sub_section=Cycling.m_def, repeats=False)


m_package.__init_metainfo__()
