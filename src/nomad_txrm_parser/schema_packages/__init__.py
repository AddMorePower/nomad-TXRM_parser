from nomad.config.models.plugins import SchemaPackageEntryPoint


class NewSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_txrm_parser.schema_packages.schema_package import m_package

        return m_package


schema_package_entry_point = NewSchemaPackageEntryPoint(
    name='TXRMSchema',
    description='Schema for TXRM files from IKTS.',
)
