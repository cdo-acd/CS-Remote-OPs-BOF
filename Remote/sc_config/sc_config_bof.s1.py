from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class SCConfigBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("sc_config")

        _error_choices = ["0", "1", "2", "3"]
        _error_choices_string = ', '.join(_error_choices)
        _start_choices = ["2", "3", "4"]
        _start_choices_string = ', '.join(_start_choices)

        self.parser.description = (
            "Configures an existing service."
        )
        self.parser.epilog = """Usage:   sc_config <SVCNAME> <BINPATH> <ERRORMODE> <STARTMODE> [--hostname HOSTNAME]
         SVCNAME      Required. The name of the service to create.
         BINPATH      Required. The binary path of the service to execute.
         ERRORMODE    Required. The error mode of the service. The valid 
                      options are:
                        0 - ignore errors
                        1 - nomral logging
                        2 - log severe errors
                        3 - log critical errors
         STARTMODE    Required. The start mode for the service. The valid
                      options are:
                        2 - auto start
                        3 - on demand start
                        4 - disabled
         HOSTNAME     Optional. The host to connect to and run the commnad on. The
                      local system is targeted if a HOSTNAME is not specified."""

        self.parser.add_argument('svcname', help=f'The name of the service to create.')
        self.parser.add_argument('binpath', help='The binary path of the service to execute.')
        self.parser.add_argument('errormode', help=f'The error mode of the service. Possible values: {_error_choices_string}')
        self.parser.add_argument('startmode', help=f'The start mode for the service. Possible values: {_start_choices_string}')
        self.parser.add_argument('--hostname', help='The host to connect to and run the command on. The local system is targeted if a HOSTNAME is not specified.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.STR, parser_arguments.hostname),
            (BOFArgumentEncoding.STR, parser_arguments.svcname),
            (BOFArgumentEncoding.STR, parser_arguments.binpath),
            (BOFArgumentEncoding.INT, parser_arguments.errormode),
            (BOFArgumentEncoding.INT, parser_arguments.startmode),
        ]
