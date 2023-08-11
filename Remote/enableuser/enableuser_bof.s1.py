from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class EnableUserBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("enableuser")

        self.parser.description = (
            "Add the specified user to the specified group."
        )
        self.parser.epilog = "Usage: enableuser <username> [--domain DOMAIN]"

        self.parser.add_argument('username', help='The user name to activate/enable.')
        self.parser.add_argument('--domain', default=str(), help='The domain/computer for the account. You must give the domain name for the user if it is a domain account, or leave empty to target an account on the local machine.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.WSTR, parser_arguments.domain),
            (BOFArgumentEncoding.WSTR, parser_arguments.username),
        ]
