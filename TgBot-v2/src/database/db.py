import os
import logging

import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

if not os.path.exists('data/'):
    os.mkdir('data/')

engine = create_engine('sqlite:///data/main.db', echo=True)
Base: declarative_base = declarative_base()

logger = logging.getLogger('my-bot')


class Users(Base):
    __tablename__ = 'USERS'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    username = Column(String)
    menu = Column(String)         # saves state of the menu the user is in
    listen_mode = Column(String)  # useful if bot shall interpret the next message in a certain way

    def __repr__(self):
        return f"<UsersEntry: username='{self.username}', chat_id='{self.chat_id}', " \
               f"menu='{self.menu}', add_mode='{self.listen_mode}', primary_key='{self.id}'"



@event.listens_for(Base.metadata, 'after_create')
def receive_after_create(target, connection, tables, **kw):
    """listen for the 'after_create' event"""
    logger.info('A table was created' if tables else 'No table was created')
    print('A table was created' if tables else 'No table was created')


def open_session() -> sqlalchemy.orm.Session:
    """
    :return: new active session
    """
    return sessionmaker(bind=engine)()


database = Base.metadata.create_all(bind=engine)
