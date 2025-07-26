
"""
    Create rebate and email data for Phoenix Bridge Club Attendance rebates.

    Get valid parameters from user and call the calculate method in process.py
"""
from root import Root

from psiutils.icecream_init import ic_init
ic_init()



def main() -> None:
    """Get the start date for the processing and initiate the processing."""
    Root()


if __name__ == '__main__':
    main()
