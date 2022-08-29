from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    private_key = os.getenv('PRIVATE_KEY')
    host = os.getenv('HOST', '0.0.0.0')
    port = os.getenv('PORT', 8000)

