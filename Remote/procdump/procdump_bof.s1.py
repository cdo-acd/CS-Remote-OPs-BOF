from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class ProcdumpBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("procdump")

        self.parser.description = (
            "Dumps the specified process to the specified output file."
        )
        self.parser.epilog = "Usage: procdump <pid> <fileout>"

        self.parser.add_argument('pid', help='The PID to dump the process of.')
        self.parser.add_argument('fileout', help='The output path to write the dump to. REMEMBER TO DELETE THIS FILE.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.INT, parser_arguments.pid),
            (BOFArgumentEncoding.WSTR, parser_arguments.fileout),
        ]
