import re
from dataclasses import asdict
from model.model import ActuacionEmail
from typing import List


def replace_placeholders_email(html_content: str, action: ActuacionEmail) -> str:
    """Replace placeholders in the email html.

    Args:
        html_content (str): Raw html.
        action (ActuacionEmail): Information to be replaced in the html.

    Returns:
        str: Raw html with the placeholders.
    """
    for placeholder, value in asdict(action).items():
        html_content = html_content.replace(
            f'{{{{ {placeholder} }}}}', str(value))
    return html_content


def split_list(lst: List[str], n: int) -> List[str]:
    """Generate different partitions of an array given a value n.

    Args:
        lst (List[str]): All strings list.
        n (int): Number of partitions.

    Yields:
        List[str]: Partition of strings.
    """

    length = len(lst)
    size = length // n
    remainder = length % n
    start = 0
    for i in range(n):
        end = start + size + (i < remainder)
        yield lst[start:end]
        start = end


def clean_string(office: str) -> str:
    """Replace double spaces to one space, and if the string ends with space, delete it.

    Args:
        office (str): Office name to be corrected.

    Returns:
        str: Corrected office name.
    """
    if "  " in office:
        office = office.replace("  ", " ")
    if office.endswith(" "):
        office = office.rstrip()
    print(office)
    return office
