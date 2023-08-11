from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class SetUserPassBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("setuserpass")

        self.parser.description = (
            "Sets the password for the specified user account on the target computer."
        )
        self.parser.epilog = """Usage:   setuserpass <USERNAME> <PASSWORD> [--domain DOMAIN]
         USERNAME  Required. The user name to activate/enable. 
         PASSWORD  Required. The new password. The password must meet GPO 
                   requirements.
         DOMAIN    Optional. The domain/computer for the account. You must give 
                   the domain name for the user if it is a domain account, or
                   empty to target an account on the local machine."""

        self.parser.add_argument('username', help=f'The user name to activate/enable.')
        self.parser.add_argument('password', help=f'The new password. The password must meet GPO requirements.')
        self.parser.add_argument('--domain', default=str(), help=f'The domain/computer for the account. You must give the domain name for the user if it is a domain account, or empty to target an account on the local machine.')
         
    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.WSTR, parser_arguments.domain),
            (BOFArgumentEncoding.WSTR, parser_arguments.username),
            (BOFArgumentEncoding.WSTR, parser_arguments.password),
        ]
