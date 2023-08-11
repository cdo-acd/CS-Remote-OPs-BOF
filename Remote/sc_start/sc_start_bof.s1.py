from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class SCStartBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("sc_start")

        self.parser.description = (
            "This command starts the specified service on the target host."
        )
        self.parser.epilog = """Usage:   sc_start <SVCNAME> [--hostname HOSTNAME]
         SVCNAME  Required. The name of the service to start.
         HOSTNAME Optional. The host to connect to and run the command on. The
                  local system is targeted if a HOSTNAME is not specified."""

        self.parser.add_argument('svcname', help=f'The name of the service to create.')
        self.parser.add_argument('--hostname', help='The host to connect to and run the command on. The local system is targeted if a HOSTNAME is not specified.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.STR, parser_arguments.hostname),
            (BOFArgumentEncoding.STR, parser_arguments.svcname),
        ]
