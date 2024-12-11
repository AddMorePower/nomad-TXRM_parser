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
from nomad.metainfo import Quantity, SchemaPackage

configuration = config.get_plugin_entry_point(
    'nomad_txrm_parser.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class TXRMOutput(Schema):
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

    operator = Quantity(type=str)
    sample_type = Quantity(type=str)
    sample_subtype = Quantity(type=str)
    sample_name = Quantity(type=str)
    elements_thickness = Quantity(type=str)
    xray_source = Quantity(type=str)
    resolution = Quantity(type=str)
    contrast = Quantity(type=str)
    project = Quantity(type=str)
    microscope_name = Quantity(type=str)


m_package.__init_metainfo__()
