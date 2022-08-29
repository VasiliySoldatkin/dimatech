from sqlalchemy.ext.asyncio import create_async_engine

host = '0.0.0.0'
password = 'root'
port = 5432
user = 'postgres'
db = 'dimatech'
engine = create_async_engine(f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}', echo=True)

