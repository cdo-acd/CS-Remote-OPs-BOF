from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class SchtasksDeleteBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("schtasks_delete", base_binary_name="schtasks_delete")

        _type_choices = ["FOLDER", "TASK"]
        _type_choices_string = ', '.join(_type_choices)

        self.parser.description = (
            "Deletes the specified scheduled task or folder."
        )
        self.parser.epilog = """Usage:   schtasks_delete <NAME> <TYPE> [--hostname HOSTNAME]
         HOSTNAME Optional. The target system (local system if not specified)
         NAME Required. The task or folder name.
         TYPE     Required. The type of target to delete. Valid options are:
                    FOLDER
                    TASK"""

        self.parser.add_argument('name', help=f'The path for the created task.')
        self.parser.add_argument('type', help=f'The type of target to delete. Possible choices: {_type_choices_string}')
        self.parser.add_argument('--hostname', default=str(), help='The host to connect to and run the command on. The local system is targeted if a HOSTNAME is not specified.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        match parser_arguments.type:
            case "TASK":
                isfolder = 0
            case "FOLDER":
                isfolder = 1

        return [
            (BOFArgumentEncoding.WSTR, parser_arguments.hostname),
            (BOFArgumentEncoding.WSTR, parser_arguments.name),
            (BOFArgumentEncoding.INT, isfolder),
        ]
