from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class SuspendBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("suspend", base_binary_name="suspendresume")

        self.parser.description = (
            "suspend a process by pid."
        )
        self.parser.epilog = """Usage: suspend <pid>

attempts to suspend the process listed"""

        self.parser.add_argument('pid', help=f'The PID to suspend.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.SHORT, 1),
            (BOFArgumentEncoding.INT, parser_arguments.pid),
        ]

class ResumeBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("resume", base_binary_name="suspendresume")

        self.parser.description = (
            "resume a process by pid."
        )
        self.parser.epilog = """Usage: resume <pid>

attempts to resume the process listed"""

        self.parser.add_argument('pid', help=f'The PID to suspend.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.SHORT, 0),
            (BOFArgumentEncoding.INT, parser_arguments.pid),
        ]
