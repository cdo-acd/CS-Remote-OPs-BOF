from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class ProcessDestroyBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("ProcessDestroy")

        self.parser.description = (
            "Closes handle(s) in a process."
        )
        self.parser.epilog = "Usage: ProcessDestroy <pid> [--handleid HANDLEID]"

        self.parser.add_argument('pid', help='The process to list the handles of. You must have permission to open the specified process.')
        self.parser.add_argument('--handleid', default=0, type=int, help='The specific handle ID to close, or close all handles if not specified. The values for HANDLEID must be between 1 - 65535.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.INT, parser_arguments.pid),
            (BOFArgumentEncoding.INT, parser_arguments.handleid),
        ]
