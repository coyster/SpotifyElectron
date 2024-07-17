"""
Date utils
"""

from datetime import datetime

date_format = "%Y-%m-%dT%H:%M:%S"

def get_current_iso8601_date() -> str:
    """Get the current date in ISO8601 format
    ISO8601 docs: https://www.iso.org/iso-8601-date-and-time-format.html

    Returns:
        str: the ISO8601 current date
    """
    current_date = datetime.now()
    date_iso8601 = current_date.strftime(date_format)
    return date_iso8601
