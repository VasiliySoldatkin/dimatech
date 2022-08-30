from sqlalchemy.ext.asyncio import create_async_engine
from config import Config

engine = create_async_engine(Config.DB_URI, echo=True)

