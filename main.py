from src.ui import user_interface_with_keyword
from src.utils import setup_and_fill_database

if __name__ == "__main__":
    """ Запуск программы"""

    db_manager = setup_and_fill_database("hh_db")
    user_interface_with_keyword(db_manager)
