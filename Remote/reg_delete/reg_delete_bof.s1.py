from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class RegDeleteBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("reg_delete")

        _hive_choices = ["HKLM", "HKCU", "HKU", "HKCR"]
        _hive_choices_string = ', '.join(_hive_choices)

        self.parser.description = (
            "Deletes the registry key or value."
        )
        self.parser.epilog = "Usage: reg_delete <hive> <path> [--value VALUE] [--hostname HOSTNAME]"

        self.parser.add_argument('hive', choices=_hive_choices, help=f'The registry hive containing the path. Possible values: {_hive_choices_string}')
        self.parser.add_argument('path', help='The registry path (deleted if value not given).')
        self.parser.add_argument('--value', default=str(), help='The registry value to delete. If the value is not specified, then the whole key is deleted.')
        self.parser.add_argument('--hostname', help='The host to connect to and run the commnad on.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        hostname = parser_arguments.hostname
        if hostname:
            hostname = "\\\\" + hostname

        match parser_arguments.hive:
            case 'HKCR':
                hive = 0
            case 'HKCU':
                hive = 1
            case 'HKLM':
                hive = 2
            case 'HKU':
                hive = 3

        value = parser_arguments.value
        if value:
            delkey = 0
        else:
            delkey = 1

        return [
            (BOFArgumentEncoding.STR, hostname),
            (BOFArgumentEncoding.INT, hive),
            (BOFArgumentEncoding.STR, parser_arguments.path),
            (BOFArgumentEncoding.STR, value),
            (BOFArgumentEncoding.INT, delkey),
        ]
