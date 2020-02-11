from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Boolean
from sqlalchemy.ext.declarative.api import declarative_base

Base = declarative_base()
SCHEMA="transactions"


class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = {'schema': 'transactions'}
    id = Column(Integer, primary_key=True)
    card_number = Column('card_number', String, nullable=False)
    pin = Column('pin', String, nullable=False)
    balance=Column('balance',Integer,nullable=False)
    public_id = Column('public_id', String, nullable=False)
    admin = Column('admin', Boolean, nullable=False)

    def __init__(self, card_number,pin,balance,public_id,admin):
        self.card_number = card_number
        self.pin = pin
        self.balance = balance
        self.public_id = public_id
        self.admin = admin

class Amount_atm(Base):
    __tablename__ = "amount_atm"
    __table_args__ = {'schema': 'transactions'}
    id = Column(Integer, primary_key=True)
    branch_name = Column('branch_name', String, nullable=False)
    denom_2000 = Column('denom_2000', Integer, nullable=False)
    denom_500 = Column('denom_500', Integer, nullable=False)
    denom_200 = Column('denom_200', Integer, nullable=False)
    denom_100 = Column('denom_100', Integer, nullable=False)
    balance=Column('balance',Integer,nullable=False)

    def __init__(self, branch_name,denom_2000,denom_500,denom_200,denom_100,balance):
        self.branch_name = branch_name
        self.denom_2000 = denom_2000
        self.denom_500 = denom_500
        self.denom_200 = denom_200
        self.denom_100 = denom_100
        self.balance = balance
