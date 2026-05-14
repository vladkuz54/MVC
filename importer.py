import asyncio
import os

from dal import engine
from dal.csv_reader import CSVReader
from dal.db_models import DBModels
from dal.repositories.db_repository import DBRepository
from generator.csv_generator import CSVGenerator

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "readings.csv")


async def main():
    generator = CSVGenerator(filename=CSV_PATH, num_rows=100)
    generator.generate_csv()

    reader = CSVReader(filename=CSV_PATH)
    data = reader.read_csv()

    models = DBModels()
    await models.drop_db()
    await models.init_db()

    repository = DBRepository(data=data)

    await repository.paste_all()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
