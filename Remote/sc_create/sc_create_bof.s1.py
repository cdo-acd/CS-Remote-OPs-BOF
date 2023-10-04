from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class SCCreateBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("sc_create")

        _error_choices = ["0", "1", "2", "3"]
        _error_choices_string = ', '.join(_error_choices)
        _start_choices = ["2", "3", "4"]
        _start_choices_string = ', '.join(_start_choices)
        _type_choices = ["1", "2", "3", "4"]
        _type_choices_string = ', '.join(_start_choices)

        self.parser.description = (
            "Creates a new service."
        )
        self.parser.epilog = """Usage:   sc_create <SVCNAME> <DISPLAYNAME> <BINPATH> <DESCRIPTION> <ERRORMODE> <STARTMODE> [--type TYPE] [--hostname HOSTNAME]
         SVCNAME      Required. The name of the service to create.
         DISPLAYNAME  Required. The display name of the service.
         BINPATH      Required. The binary path of the service to execute.
         DESCRIPTION  Required. The description of the service.
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
         TYPE         Optional. The type of service to create. The valid
                      options are:
                      1 - SERVICE_FILE_SYSTEM_DRIVER (File system driver service)
                      2 - SERVICE_KERNEL_DRIVER (Driver service)
                      3 - SERVICE_WIN32_OWN_PROCESS (Service that runs in its own process) <-- Default
                      4 - SERVICE_WIN32_SHARE_PROCESS (Service that shares a process with one or more other services)
         HOSTNAME     Optional. The host to connect to and run the commnad on. The
                      local system is targeted if a HOSTNAME is not specified."""

        self.parser.add_argument('svcname', help=f'The name of the service to create.')
        self.parser.add_argument('displayname', help=f'The display name of the service.')
        self.parser.add_argument('binpath', help='The binary path of the service to execute.')
        self.parser.add_argument('description', help='The description of the service.')
        self.parser.add_argument('errormode', help=f'The error mode of the service. Possible values: {_error_choices_string}')
        self.parser.add_argument('startmode', help=f'The start mode for the service. Possible values: {_start_choices_string}')
        self.parser.add_argument('--type', default=3, type=int, help=f'The type of service to create. Possibel values: {_type_choices_string}')
        self.parser.add_argument('--hostname', help='The host to connect to and run the command on. The local system is targeted if a HOSTNAME is not specified.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        match parser_arguments.type:
            case 1:
                serviceType = 0x02
            case 2:
                serviceType = 0x01
            case 3:
                serviceType = 0x10
            case 4:
                serviceType = 0x20
            case _:
                serviceType = 0x10

        return [
            (BOFArgumentEncoding.STR, parser_arguments.hostname),
            (BOFArgumentEncoding.STR, parser_arguments.svcname),
            (BOFArgumentEncoding.STR, parser_arguments.binpath),
            (BOFArgumentEncoding.STR, parser_arguments.displayname),
            (BOFArgumentEncoding.STR, parser_arguments.description),
            (BOFArgumentEncoding.INT, parser_arguments.errormode),
            (BOFArgumentEncoding.INT, parser_arguments.startmode),
            (BOFArgumentEncoding.INT, serviceType),
        ]
