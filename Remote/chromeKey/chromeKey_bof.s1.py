from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class ChromeKeyBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("chromeKey")

        self.parser.description = (
            "Decrypts the provided base64 encoded Chrome key"
        )
        self.parser.epilog = "Usage: chromeKey"
