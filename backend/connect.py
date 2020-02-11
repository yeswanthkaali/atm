import logging
import os

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative.api import declarative_base

Base = declarative_base()
SCHEMA = "transactions"
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
URL = os.getenv('URL')
DB=os.getenv('DB')


class DbConnect:

    def __init__(self):
        try:
            self.autocommit = False
            self.autoflush = False
            self.debug = False
            self.connect_str = self.build_connection_string()
            self.engine = create_engine(self.connect_str)
            session = scoped_session(sessionmaker(autocommit=self.autocommit,
                                                  autoflush=self.autoflush, bind=self.engine))
            self.session = session()
        except Exception as err:
            logging.error("DB Error : %s", err)

    @staticmethod
    def build_connection_string():
        return "postgresql://{}:{}@{}/{}" \
            .format(USER,PASSWORD,URL,
                    DB)

    def close(self):
        if (self.session):
            self.session.close()
