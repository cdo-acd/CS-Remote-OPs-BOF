from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class RegSaveBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("reg_save")

        _hive_choices = ["HKLM", "HKCU", "HKU", "HKCR"]
        _hive_choices_string = ', '.join(_hive_choices)

        self.parser.description = (
            "Saves the registry path and all subkeys to disk."
        )
        self.parser.epilog = "Usage: reg_save <hive> <path> <fileout>"

        self.parser.add_argument('hive', choices=_hive_choices, help=f'The registry hive containing the path. Possible values: {_hive_choices_string}')
        self.parser.add_argument('path', help='The registry path (deleted if value not given).')
        self.parser.add_argument('fileout', help='The output file. FILEOUT IS SAVED TO DISK ON TARGET, CLEAN IT UP.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        match parser_arguments.hive:
            case 'HKCR':
                hive = 0
            case 'HKCU':
                hive = 1
            case 'HKLM':
                hive = 2
            case 'HKU':
                hive = 3

        return [
            (BOFArgumentEncoding.STR, parser_arguments.path),
            (BOFArgumentEncoding.STR, parser_arguments.fileout),
            (BOFArgumentEncoding.INT, hive),
        ]
