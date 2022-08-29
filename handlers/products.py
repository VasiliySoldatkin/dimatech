from sanic.request import Request
from sanic.response import HTTPResponse, text, json
from sanic.views import HTTPMethodView
from db.models import Products
from serializers.schemas import ProductSchema
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sanic_jwt import protected, inject_user
from db.engine import engine
from functools import wraps
from typing import Optional
from utils.auth import check_permission




class ProductsView(HTTPMethodView):
    decorators = [protected(), inject_user(), check_permission()]

    async def patch(self, request: Request, user: dict, product_id: Optional[int] = None) -> HTTPResponse:
        schema = ProductSchema()
        async_session = sessionmaker(engine, class_=AsyncSession)
        result = []
        async with async_session() as session:
            products = await session.execute(select(Products))
            for product in products.fetchall():
                print(product[0])
                result.append(schema.dump(product[0]))
            await session.commit()
        return json(result)

    async def get(self, request: Request, user: dict, product_id: Optional[int] = None) -> HTTPResponse:
        schema = ProductSchema()
        async_session = sessionmaker(engine, class_=AsyncSession)
        result = []
        # поправить это все
        async with async_session() as session:
            stmt = select(Products) if product_id is None else select(Products).where(Products.id == product_id)
            products = await session.execute(stmt)
            for product in products.fetchall():
                print(product[0])
                result.append(schema.dump(product[0]))
            await session.commit()
        return json(result)

    async def post(self, request: Request, user: dict) -> HTTPResponse:
        # 4.1 Создавать товары (админ)
        schema = ProductSchema()
        result = schema.dump(request.json)
        async_session = sessionmaker(engine, class_=AsyncSession)
        async with async_session() as session, session.begin():
            await session.execute(insert(Products).values(result))
        return json({'OK': True})

    async def delete(self, request: Request, user: dict, product_id: Optional[int] = None) -> HTTPResponse:
        schema = ProductSchema()
        result = schema.dump(request.json)
        async_session = sessionmaker(engine, class_=AsyncSession)
        async with async_session() as session, session.begin():
            await session.execute(insert(Products).values(result))
        return json({'OK': True})
