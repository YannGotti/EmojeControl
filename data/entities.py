#from sqlalchemy import DateTime, create_engine, Integer, String, \
#    Column, ForeignKey, Boolean, ARRAY, BigInteger
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship
#from sqlalchemy_utils import database_exists, create_database

#from config import CONNECTION_STRING

##engine = create_engine(CONNECTION_STRING)

##if not database_exists(engine.url):
   # create_database(engine.url)

##Base = declarative_base()

##class User(Base):
 #   __tablename__ = 'users'
   ## id = Column(Integer(), primary_key=True)
   ## chat_id = Column(BigInteger(), nullable=False)
   ## twitch_name = Column(String(100), nullable=True)
   ## money = Column(BigInteger(), nullable=False, default=10000)
   ## select_color = Column(String(100), nullable=False, default="Нет")
   ## bet = Column(BigInteger(), nullable=False, default = 0)
   ## current_message_game_id = Column(BigInteger(), nullable=False, default = 0)


##class Game(Base):
   ## __tablename__ = 'game'
   ## id = Column(Integer(), primary_key=True)
  ##  win_color = Column(String(100), nullable=True)
  ##  isBet = Column(Boolean, nullable=False, default=False)

##Base.metadata.create_all(engine)