from sanic import Sanic
from sanic_jwt import Initialize
from handlers import router, error_handler, auth
from handlers import admin_bp, my_bp
from config import Config
from db.engine import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert
from db.models import Users

app = Sanic('dimatech_test')
app.error_handler = error_handler
app.router = router
app.blueprint(admin_bp)
app.blueprint(my_bp)
Initialize(app, secret=Config.PRIVATE_KEY, authenticate=auth.jwt_auth,
           class_views=(('/register', auth.Register), # Регистрация и возвращение ссылки активации
                        ('/register/verify', auth.VerifyUser)), # Активация аккаунта
           custom_claims=[auth.AdminClaim, auth.ActiveClaim],
           retrieve_user=auth.retrieve_user)


@app.before_server_start
async def create_admin(*args, **kwargs):
    stmt = select(Users).filter(Users.admin == True)
    async_session = sessionmaker(engine, AsyncSession)
    async with async_session() as session:
        data = (await session.execute(stmt)).first()
        if data:
            return
        stmt = insert(Users).values(login=Config.ADMIN_LOGIN, password=Config.ADMIN_PASSWORD,
                                    is_active=True, admin=True).returning(Users)
        admin = (await session.execute(stmt)).first()

        await session.commit()

app.run(host='0.0.0.0', port=8000)
