from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class OfficeTokensBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("office_tokens")

        self.parser.description = (
            "Searches memory for Office JWT Access Tokens."
        )
        self.parser.epilog = "Usage: office_tokens <pid>"

        self.parser.add_argument('pid', help='The PID to search the memory of.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.INT, parser_arguments.pid),
        ]
