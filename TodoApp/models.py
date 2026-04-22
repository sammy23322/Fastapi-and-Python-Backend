from database import Base
from sqlalchemy import INTEGER, String, Boolean, Column , ForeignKey



class Todos(Base):

    __tablename__ = "Todos"

    id = Column(INTEGER, primary_key = True, index = True)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    complete = Column(Boolean, default=False)
    owner_id = Column(INTEGER , ForeignKey("Users.id"))

class Users(Base):

    __tablename__ = "Users"

    id = Column(INTEGER, primary_key = True, index = True)
    email = Column(String , unique= True)
    user_name = Column(String , unique= True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default= True)
    role = Column(String)