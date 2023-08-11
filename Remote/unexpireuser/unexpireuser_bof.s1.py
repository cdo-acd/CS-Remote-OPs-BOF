from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class UnexpireUserBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("unexpireuser")

        self.parser.description = (
            "Activates (and if necessary enables) the specified user account on the target computer."
        )
        self.parser.epilog = """Usage:   unexpireuser <USERNAME> [--domain DOMAIN]
         USERNAME  Required. The user name to activate/enable. 
         DOMAIN    Optional. The domain/computer for the account. You must give 
                   the domain name for the user if it is a domain account, or
                   ommitted to targent a local user."""

        self.parser.add_argument('username', help=f'The user name to activate/enable')
        self.parser.add_argument('--domain', help=f'The domain/computer for the account.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.WSTR, parser_arguments.domain),
            (BOFArgumentEncoding.WSTR, parser_arguments.username),
        ]
