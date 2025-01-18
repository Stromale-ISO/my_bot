import asyncpg
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#parameters for connect
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))


#create a connection pool with parameters
async def create_db_pool():
    try:

        logger.info(f"Connecting to database {DB_NAME} at {DB_HOST}:{DB_PORT} as {DB_USER}")
        pool = await asyncpg.create_pool(
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT,
            ssl=False,
            timeout=10
        )
        logger.info("Database pool created successfully!")
        return pool
    except Exception as e:
        logger.error(f"Error creating database pool: {e}")
        raise


db_pool = None
#chech for pool be on
async def get_db_pool():
    global db_pool
    if not db_pool:
        db_pool = await create_db_pool()
    return db_pool

async def add_person(name, surname, birthdate, description):
    pool = await get_db_pool()#connect connection pool
    async with pool.acquire() as conn: #use one connection from pool
        birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d").date()
        await conn.execute(
            "INSERT INTO persons (person_name, person_surname, person_birthdate, person_description) VALUES ($1, $2, $3, $4)",
            name ,surname, birthdate_obj, description
        )


async def delete_person(person_id):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM persons WHERE person_id = $1",
            person_id
        )


async def get_all_persons():
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM persons ORDER BY person_id ASC")
        print(rows)
        return rows


async def get_persons_by_month(month: str):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT * FROM persons
            WHERE EXTRACT(MONTH FROM person_birthdate) = $1
            """, int(month)
        )
        return rows


async def update_description(person_id: int, new_description: str):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "UPDATE persons SET person_description = $1 WHERE person_id = $2",
            new_description, person_id
        )
        if result == "UPDATE 0":
            raise ValueError("Запись с таким ID не найдена. Пошел отсюда.")
        await conn.execute("CLUSTER persons USING persons_pkey")

async def check_person_exists(person_id: int) -> bool:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        result = await conn.fetchval("SELECT COUNT(*) FROM persons WHERE person_id = $1", person_id)
        return result > 0