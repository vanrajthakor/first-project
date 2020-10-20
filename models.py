from sqlalchemy import Column, Integer, String,Date,Text
from sqlalchemy import create_engine
engine = create_engine('sqlite:///bot.db', echo = True,connect_args={'check_same_thread': False})
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    date = Column(Date)
    first_name= Column(String)
    last_name=Column(String)
    username = Column(String)

    def __str__(self):
        return "{} {} (@{})".format(self.first_name, self.last_name, self.username)

class Channel(Base):
    __tablename__ = 'channel'
    id = Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    channel_id=Column(Integer)
    channel=Column(String)
    subscribers=Column(Integer)
    channel_name=Column(String)
    admin_username = Column(String)
    description=Column(String)
    
    def __str__(self):
        
        return f'\nChannel Id : {self.channel_id}\nChannel Name : {self.channel_name}\nUsername : {self.channel}\nSubscribers : {self.subscribers}'
    
class Ban(Base):
    __tablename__ = 'ban'
    id = Column(Integer, primary_key=True)
    username=Column(String)

    def __repr__(self):
        
        return f'{self.id}.{self.username}'

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    emoji=Column(String)
    set_top=Column(String)
    set_bottom=Column(String)
    set_button_name=Column(String)
    set_button_url=Column(String)
    set_caption=Column(String)


    def __repr__(self):
        
        return f'{self.emoji}{self.set_top}{self.set_bottom}{self.set_button_name}{self.set_buttom_url}{self.set_caption}'

class Button(Base):
    __tablename__ = 'button'
    id = Column(Integer, primary_key=True)
    chat_id=Column(Integer)
    set_button_name=Column(String)
    set_button_url=Column(String)

class Promo(Base):
    __tablename__ = 'promo'
    id = Column(Integer, primary_key=True)
    channel=Column(Integer)
    message_id=Column(Integer)

Base.metadata.create_all(engine)

