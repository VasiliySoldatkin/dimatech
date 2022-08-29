from sanic.request import Request
from sanic.response import HTTPResponse, json

from db.engine import engine
from db.models import Transactions, Accounts, Users
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from serializers.schemas import PaymentSchema, BuyProductSchema
from sqlalchemy import select, insert, update
from cryptohash import sha1
from config import Config


async def payment_webhook(request: Request) -> HTTPResponse:
    async_session = sessionmaker(engine, class_=AsyncSession)
    body = request.json
    result = PaymentSchema().load(body)
    insert_stmt = insert(Accounts).values(
        user_id=result['user_id'],
        id=result['bill_id'],
        balance=result['amount'])

    stmt = update(Accounts).filter(Accounts.id == result['bill_id']).filter(
        Accounts.user_id == result['user_id']).values(
        balance=Accounts.balance + result['amount'])
    select_stmt = select(Accounts).filter(Accounts.id == result['bill_id']).filter(
        Accounts.user_id == result['user_id'])
    transaction_stmt = insert(Transactions).values(amount=result['amount'], account_id=result['bill_id']).returning(
        Transactions.id)

    async with async_session() as session:
        select_cursor = await session.execute(select_stmt)
        if select_cursor.first() is None:
            stmt = insert(Accounts).values(
                id=result['bill_id'],
                balance=result['amount'],
                user_id=result['user_id']
            )
        stmt = stmt.returning(Accounts)

        # Обрабатывать ошибки ForeignKey и другие
        cursor = await session.execute(stmt)

        resp = dict(zip(('amount', 'bill_id', 'user_id'), cursor.first()))
        transaction_id = (await session.execute(transaction_stmt)).first()[0]

        resp['signature'] = sha1(
            f'{Config.private_key}:{transaction_id}:{result["user_id"]}:{result["bill_id"]}:{result["amount"]}')
        resp['transaction_id'] = transaction_id

        await session.commit()

    return json(resp)


# Сделать проверку на возможность снятия счета с такого юзера (чтобы другие юзеры не снимали деньги не со своих счетов)
async def buy_product(request: Request, product_id):
    body = request.json
    k = BuyProductSchema().load(body)
    async_session = sessionmaker(engine, class_=AsyncSession)
    buy_product_stmt = update(Accounts).filter(Accounts.id == request)

async def get_transaction_history(request: Request) -> HTTPResponse:
    # 5. Получить историю транзакций
    ...