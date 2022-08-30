from sanic.request import Request
from sanic.response import HTTPResponse, json

from db.engine import engine
from db.models import Transactions, Accounts, Users, Products
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
            f'{Config.PRIVATE_KEY}:{transaction_id}:{result["user_id"]}:{result["bill_id"]}:{result["amount"]}')
        resp['transaction_id'] = transaction_id

        await session.commit()

    return json(resp)


# Сделать проверку на возможность снятия счета с такого юзера (чтобы другие юзеры не снимали деньги не со своих счетов)
async def buy_product(request: Request, product_id):
    data = BuyProductSchema().load(request.json)
    async_session = sessionmaker(engine, class_=AsyncSession)

    get_price = select(Products.price).filter(Products.id == product_id)
    async with async_session() as session:
        price = (await session.execute(get_price)).first()
        if not price:
            return json({
                'error': 'not such product', 'code': 400
            }, status=400)
        buy_product_stmt = update(Accounts).filter(Accounts.id == data['account_id']). \
            values(balance=Accounts.balance - price[0]).returning(Accounts.balance)

        resp = (await session.execute(buy_product_stmt)).first()
        if not resp:
            return json({
                'error': 'no such account', 'code': 400
            }, status=400)
        resp = resp[0]
        if resp < 0:
            return json({
                'error': 'not enough money', 'code': 400
            }, status=400)

        await session.commit()
    return json({
        'balance': resp
    })


async def get_transaction_history(request: Request, account_id: int) -> HTTPResponse:
    get_history = select(Transactions).filter(Transactions.account_id == account_id)
    async_session = sessionmaker(engine, class_=AsyncSession)
    result = []
    async with async_session() as session:
        cursor = (await session.execute(get_history)).all()
        for item in cursor:
            transaction: Transactions = item[0]
            resp_transaction = {'id': transaction.id, 'account_id': transaction.account_id, 'amount': transaction.amount}
            result.append(resp_transaction)

    return json(result)
