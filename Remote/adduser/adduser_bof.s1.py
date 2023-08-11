from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class AddUserBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("adduser")

        self.parser.description = (
            "Add a new user to a machine."
        )
        self.parser.epilog = "Usage: adduser <username> <password> [--server server]"

        self.parser.add_argument('username', help='The name of the new user.')
        self.parser.add_argument('password', help='The password of the new user.')
        self.parser.add_argument('--server', default=str(), help='If entered, the user will be created on that machine. If not, the local machine will be used.')

    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.WSTR, parser_arguments.username),
            (BOFArgumentEncoding.WSTR, parser_arguments.password),
            (BOFArgumentEncoding.WSTR, parser_arguments.server)
        ]
