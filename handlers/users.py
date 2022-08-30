from sanic.request import Request
from sanic.response import HTTPResponse, json
from db.models import Users, Accounts
from sanic_jwt import inject_user, protected
from sqlalchemy.orm import sessionmaker, contains_eager
from db.engine import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from utils.auth import check_active


@check_active()
@inject_user()
@protected()
async def get_accounts_and_history(request: Request, user: dict, **kwargs) -> HTTPResponse:
    async_session = sessionmaker(engine, class_=AsyncSession)
    stmt = select(Users).join(Users.accounts).join(Accounts.transactions). \
        options(contains_eager(Users.accounts),
                contains_eager(Users.accounts, Accounts.transactions)).\
        filter(Users.id == user['user_id'])

    result = []
    async with async_session() as session:
        data = (await session.execute(stmt)).unique().scalars()
        print(data)
        for user in data:
            user_data = {'id': user.id, 'login': user.login, 'is_active': user.is_active, 'accounts': []}
            for account in user.accounts:
                data_account = {'id': account.id, 'balance': account.balance, 'transactions': []}
                for transaction in account.transactions:
                    data_transaction = {'id': transaction.id, 'amount': transaction.amount}
                    data_account['transactions'].append(data_transaction)
                user_data['accounts'].append(data_account)
            result.append(user_data)
        await session.commit()

    return json(result)
