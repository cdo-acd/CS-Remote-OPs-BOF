from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class AddUserToGroupBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("addusertogroup")

        self.parser.description = (
            "Add the specified user to the specified group."
        )
        self.parser.epilog = "Usage: addusertogroup <username> <groupname> [--server server] [--domain domain]"

        self.parser.add_argument('username', help='The user name to activate/enable.')
        self.parser.add_argument('groupname', help='The group to add the user to.')
        self.parser.add_argument('--server', default=str(), help='The target computer to perform the addition on. Leave empty for the local machine.')
        self.parser.add_argument('--domain', default=str(), help='The domain/computer for the account. You must give the domain name for the user if it is a domain account or leave empty for a local user.')

    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.WSTR, parser_arguments.domain),
            (BOFArgumentEncoding.WSTR, parser_arguments.server),
            (BOFArgumentEncoding.WSTR, parser_arguments.username),
            (BOFArgumentEncoding.WSTR, parser_arguments.groupname),
        ]
