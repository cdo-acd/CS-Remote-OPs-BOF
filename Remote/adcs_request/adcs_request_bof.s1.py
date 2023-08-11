from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class ADCSRequestBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("adcs_request")

        self.parser.description = (
            "This command connects a certificate authority and requests an enrollment certificate of the specified type for the specified subject and alternative name. It will also optionally install the certificate for the current context."
        )
        self.parser.epilog = "Usage: adcs_request <CA> [--template TEMPLATE] [--subject SUBJECT] [--altname ALTNAME] [--install] [--machine]"

        self.parser.add_argument('ca', help='The certificate authority to use.')
        self.parser.add_argument('--template', help='The certificate type to request.')
        self.parser.add_argument('--subject', help='The subject\'s distinguished name.')
        self.parser.add_argument('--altname', help='The alternate subject\'s distinguished name.')
        self.parser.add_argument('--install', action='store_true', help='Install the certificate in current context?')
        self.parser.add_argument('--machine', action='store_true', help='Request a certificate for a machine instead of a user?')

    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        return [
            (BOFArgumentEncoding.WSTR, parser_arguments.ca),
            (BOFArgumentEncoding.WSTR, parser_arguments.template),
            (BOFArgumentEncoding.WSTR, parser_arguments.subject),
            (BOFArgumentEncoding.WSTR, parser_arguments.altname),
            (BOFArgumentEncoding.INT, 1 if parser_arguments.install else 0),
            (BOFArgumentEncoding.INT, 1 if parser_arguments.machine else 0),
        ]
