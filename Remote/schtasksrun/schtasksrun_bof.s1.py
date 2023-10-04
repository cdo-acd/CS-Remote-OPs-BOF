from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class SchtasksRunBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("schtasks_run", base_binary_name="schtasksrun")

        self.parser.description = (
            "Run the specified scheduled task."
        )
        self.parser.epilog = """Usage:   schtasks_run <TASKNAME> [--hostname HOSTNAME]
         HOSTNAME  Optional. The target system (local system if not specified)
         TASKNAME  Required. The scheduled task name."""

        self.parser.add_argument('name', help=f'The path for the created task.')
        self.parser.add_argument('--hostname', default=str(), help='The host to connect to and run the command on. The local system is targeted if a HOSTNAME is not specified.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.WSTR, parser_arguments.hostname),
            (BOFArgumentEncoding.WSTR, parser_arguments.name),
        ]
