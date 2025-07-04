from configparser import ConfigParser
import os
from typing import Dict


def config(filename="database.ini", section="postgresql") -> Dict[str, str]:
    """Получаем параметры подключения к базе данных из файла конфигурации"""

    if filename is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = os.path.join(base_dir, "database.ini")

    parser = ConfigParser()
    with open(filename, encoding="utf-8") as f:
        parser.read_file(f)

    db: Dict[str, str] = {}
    if parser.has_section(section):
        for key, value in parser.items(section):
            clean_value = value.strip()
            if isinstance(clean_value, bytes):
                clean_value = clean_value.decode("utf-8", errors="replace")
            db[key] = clean_value
    else:
        raise Exception(f"Section {section} not found in the {filename} file.")
    return db


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/133.0.0.0 Safari/537.36 "
    "OPR/118.0.0.0 (Edition std-2)"
)
