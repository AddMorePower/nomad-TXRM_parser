from nomad.config.models.plugins import ParserEntryPoint


class NewParserEntryPoint(ParserEntryPoint):

    def load(self):
        from nomad_txrm_parser.parsers.parser import NewParser

        return NewParser(**self.dict())


parser_entry_point = NewParserEntryPoint(
    name='TXRMParser',
    description='Parser for .txrm files from IKTS.',
    mainfile_name_re='.*\.txrm',
)
