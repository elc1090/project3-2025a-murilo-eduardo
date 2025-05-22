from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

engine = create_engine("sqlite:///:memory:", echo=True)
# engine = create_engine('sqlite:///example.db', echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    content = Column(Text(), nullable=True)

    def __repr__(self):
        return f"<Component(name='{self.name}', content='{self.content}')>"


class UserComponent(Base):
    __tablename__ = "users_components"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    component_id = Column(Integer, ForeignKey("components.id"), primary_key=True)

    def __repr__(self):
        return f"<UserComponent(user_id='{self.user_id}', component_id='{self.component_id}')>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    def __repr__(self):
        return f"<User(name='{self.username}', password='{self.password}')>"


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_user(session, username, password):
    user = User(username=username, password=hash_password(password))

    session.add(user)
    session.commit()

    return user


def delete_user(session, username):
    pass


def authenticate_user(session, username, password):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        return False
    return verify_password(password, user.password)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
