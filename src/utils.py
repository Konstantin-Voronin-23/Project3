from typing import Any, Dict

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from src.company import Company
from config import config
from src.db_manager import DBManager
from src.hh_api import HeadHunterAPI
from src.vacancy import Vacancy


def create_database(db_name: str) -> None:
    """Создаёт базу данных, если она ещё не существует"""

    params: Dict[str, Any] = config()
    params["dbname"] = "postgres"
    conn = psycopg2.connect(**params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", (db_name,))
            exists = cur.fetchone()
            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                print(f"База данных '{db_name}' успешно создана.")
            else:
                print(f"База данных '{db_name}' уже существует.")
    finally:
        conn.close()


def fill_database_with_api_data(db_manager: DBManager, api: HeadHunterAPI) -> None:
    """Запрашивает у пользователя ключевое слово для поиска, загружает компании и вакансии из API HeadHunter,
    и добавляет их в базу данных"""

    keyword = input("Введите ключевое слово для поиска компаний и вакансий: ").strip()
    if not keyword:
        print("Ключевое слово не может быть пустым. Завершение работы.")
        exit()

    companies = api.get_employers(keyword, per_page=10)
    for company_data in companies:
        company = Company.from_api_data(company_data)
        vacancies = api.get_vacancies(keyword, per_page=10)
        if vacancies:
            db_manager.insert_company(company)
            for vacancy_data in vacancies:
                vacancy = Vacancy.from_api_data(vacancy_data)
                db_manager.insert_vacancy(vacancy, company.company_id)
    print("Данные успешно загружены и сохранены в базу.")


def setup_and_fill_database(db_name: str = "hh_db") -> DBManager:
    """
    Полная инициализация базы: создание, создание таблиц, заполнение данными.
    """

    create_database(db_name)
    db_manager = DBManager(dbname=db_name)
    db_manager.create_tables()
    api = HeadHunterAPI()
    fill_database_with_api_data(db_manager, api)
    return db_manager
