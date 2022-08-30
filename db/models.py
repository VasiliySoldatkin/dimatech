from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, SmallInteger, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
from sqlalchemy_utils import ChoiceType

Base = declarative_base()


# Сделать Optimistic Lock

class Users(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, autoincrement=True, index=True)
    login = Column('login', String(100), unique=True, index=True)
    password = Column('password', String(250))
    is_active = Column('is_active', Boolean, default=False)
    admin = Column('admin', Boolean, default=False)
    accounts = relationship('Accounts')


class Roles(Base):
    __tablename__ = 'roles'
    id = Column('id', SmallInteger, primary_key=True, autoincrement=True)
    name = Column('name', String(20))


class Products(Base):
    __tablename__ = 'products'
    id = Column('id', Integer, primary_key=True, autoincrement=True, index=True)
    title = Column('title', String(100), index=True)
    price = Column('price', Float)


class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column('id', Integer, primary_key=True, index=True)
    balance = Column('balance', Float, CheckConstraint('balance >= 0.0'), default=0.0)
    user_id = Column('user_id', Integer, ForeignKey("users.id"))
    transactions = relationship('Transactions')


class Transactions(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column('amount', Float)
    account_id = Column(Integer, ForeignKey('accounts.id'))
