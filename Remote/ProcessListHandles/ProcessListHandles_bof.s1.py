from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class ProcessListHandlesBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("ProcessListHandles")

        self.parser.description = (
            "Lists open handles in process."
        )
        self.parser.epilog = "Usage: ProcessListHandles <pid>"

        self.parser.add_argument('pid', help='The process to list the handles of. You must have permission to open the specified process.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.INT, parser_arguments.pid),
        ]
