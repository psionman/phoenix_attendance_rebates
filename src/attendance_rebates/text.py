"""
Text module that merges psiutils.text.strings with project-level strings.

Usage:
    from text_module import Text

    txt = Text()
    print(txt.SELECT)   # Access as attribute
    print(txt.DELETE_PROMPT)
"""

from dataclasses import dataclass, field
from psiutils.text import Text as PsiText

strings = {
    'ACCEPT': 'Accept',
    'BBO': 'bbo',
    'CF_PREFIX': 'cf',
    'CLUB': 'CLUB',
    'CONFIG': 'Settings',
    'CSV': 'csv',
    'DELETE_PROMPT': 'Are you sure you wish to delete this record?',
    'DIRECTORS': 'Director\'s',
    'EMAIL': 'email',
    'F2F': 'f2f',
    'HIDE': 'Hide',
    'MEMBERSHIP': 'membership',
    'PLAYERS': 'Player\'s',
    'REBATE_REPORT': 'att_report',
    'REBATE_FILE_PREFIX': 'att_rebate',
    'RESET': 'reset',
    'SELECT': 'Select',
    'SHOW': 'Show',
    'TITLE': 'Players\' Attendance Rebates',
    'VERIFY': 'Verify',
}


@dataclass
class Text:
    """Combines package-level (psiutils) and project-level strings.

    Attributes from `psiutils.text.strings` are loaded first, then overridden
    or extended by the local `strings` dictionary.
    """

    display: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        """Populate the dataclass instance with string attributes."""
        # Load psiutils strings
        psi_text = PsiText()
        psi_strings = psi_text.strings
        for key, string in psi_strings.items():
            setattr(self, key, string)

        # Override or add project-level strings
        for key, string in strings.items():
            setattr(self, key, string)

        # Optionally display contents of `text`
        if self.display:
            psi_text.display(strings)
