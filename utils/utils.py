import re
from dataclasses import  asdict
from model.ActuacionEmail import ActuacionEmail

def get_defendant_and_plaintiff(plain_def:str) -> tuple[str, str]:
    """Obtain the plaintiff and defendant names by a string.

    Args:
        plain_def (str): Information with the defendant and plaintiff

    Returns:
        tuple[str, str]: Plaintiff and defendant names.
    """
    plaintiff_pattern = re.compile(r'Demandante: (.+?) \|')
    defendant_pattern = re.compile(r'Demandado: (.+?)$')
    is_plaintiff = plaintiff_pattern.search(plain_def)
    is_defendant = defendant_pattern.search(plain_def)
    if is_plaintiff:
        plaintiff = is_plaintiff.group(1)
    else:
        plaintiff = None

    if is_defendant:
        defendant = is_defendant.group(1)
    else:
        defendant = None

    return plaintiff,defendant

def replace_placeholders_email(html_content:str, action: ActuacionEmail):
    for placeholder, value in asdict(action).items():
        html_content = html_content.replace(f'{{{{ {placeholder} }}}}', str(value))
    return html_content
