from typing import Dict, List, Optional, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.exceptions import TaskInvalidArgumentsException


class SchtasksCreateBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("schtaskscreate")

        _user_choices = ["USER", "XML", "SYSTEM"]
        _user_choices_string = ', '.join(_user_choices)
        _force_choices = ["CREATE", "UPDATE"]
        _force_choices_string = ', '.join(_force_choices)

        self.parser.description = (
            "Creates a new scheduled task."
        )
        self.parser.epilog = """Usage:   schtaskscreate <name> <user> <force> [--hostname HOSTNAME]
         HOSTNAME  Optional. The system on which to create the task.
         NAME  Required. The path for the created task.
         USER  Required. The username to associate with the task. The valid
                   options are (case sensitive):
                     USER uses the current user
                     XML uses the principal user from the task XML
                     SYSTEM uses the Local System service
         FORCE Required. Creation disposition. The options are (case 
                   sensitive):
                     CREATE fail if the task already exists
                     UPDATE update an exiting task"""

        self.parser.add_argument('name', help=f'The path for the created task.')
        self.parser.add_argument('user', help=f'The username to associate with the task. Possible choices: {_user_choices_string}')
        self.parser.add_argument('force', help=f'Creation disposition. Possible choices: {_force_choices_string}')
        self.parser.add_argument('--hostname', default=str(), help='The host to connect to and run the command on. The local system is targeted if a HOSTNAME is not specified.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        match parser_arguments.user:
            case "USER":
                user = 0
            case "SYSTEM":
                user = 1
            case "XML":
                user = 2

        match parser_arguments.force:
            case "UPDATE":
                force = 1
            case "CREATE":
                force = 0

        xml = self.get_file_by_name("xml")

        return [
            (BOFArgumentEncoding.WSTR, parser_arguments.hostname),
            (BOFArgumentEncoding.WSTR, parser_arguments.name),
            (BOFArgumentEncoding.WSTR, xml.content),
            (BOFArgumentEncoding.INT, user),
            (BOFArgumentEncoding.INT, force),
        ]

    def validate_files(self, arguments: List[str]):
        xml_file = self.get_file_by_name("xml")

        if xml_file is None:
            raise TaskInvalidArgumentsException("No .xml file uploaded.")

    def get_gui_elements(self) -> Optional[Dict]:
        return {
            "title": "schtaskscreate by Trustedsec",
            "desc": "Using schtaskscreate BOF by Trustedsec to create a scheduled task on the local/remote host.",
            "elements": [
                {
                    "name": "xml",
                    "type": "file",
                    "description": "XML",
                    "placeholder": "Select .xml File",
                },
            ],
        }