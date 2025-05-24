from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import event

from flask import Flask, request, jsonify

app = Flask(__name__)

# engine = create_engine("sqlite:///:memory:", echo=True)
engine = create_engine("sqlite:///uinify.db", echo=True)
conn = engine.connect()

Session = sessionmaker(bind=engine)
Base = declarative_base()


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    content = Column(Text(), nullable=True)

    def __repr__(self):
        return f"<Component(name='{self.name}', content='{self.content}')>"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "content": self.content}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    components = relationship(
        "UserComponent",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"<User(name='{self.username}', password='{self.password}')>"

    def to_dict(self):
        return {"id": self.id, "username": self.username}


class UserComponent(Base):
    __tablename__ = "users_components"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    component_id = Column(
        Integer, ForeignKey("components.id", ondelete="CASCADE"), primary_key=True
    )

    user = relationship("User", back_populates="components")

    def __repr__(self):
        return f"<UserComponent(user_id='{self.user_id}', component_id='{self.component_id}')>"


Base.metadata.create_all(engine)


@app.route("/users", methods=["GET"])
def users_get():
    with Session() as session:
        try:
            users = session.query(User).all()
            return jsonify([user.to_dict() for user in users]), 200
        except Exception as e:
            return jsonify(error=str(e)), 500


@app.route("/user", methods=["POST"])
def user_post():
    r = request.get_json()

    for key in ["username", "password"]:
        if key not in r:
            return jsonify(error=f"Missing '{key}' key."), 400

    with Session() as session:
        try:
            user = User(username=r["username"], password=r["password"])
            session.add(user)
            session.commit()
            return jsonify(user.to_dict()), 200
        except Exception as e:
            session.rollback()
            return jsonify(error=str(e)), 500


@app.route("/user/<int:id>", methods=["GET"])
def user_get(id):
    with Session() as session:
        try:
            user = session.query(User).filter_by(id=id).first()
            if user is None:
                return jsonify(error=f"User '{id}' not found."), 404
            return user.to_dict(), 200
        except Exception as e:
            return jsonify(error=str(e)), 500


@app.route("/user/<int:id>", methods=["DELETE"])
def user_delete(id):
    with Session() as session:
        try:
            user = session.get(User, id)
            if user is None:
                return jsonify(error=f"User '{id}' not found."), 404
            session.delete(user)
            session.commit()
            return jsonify(user.to_dict()), 200
        except Exception as e:
            session.rollback()
            return jsonify(error=str(e)), 500


@app.route("/user/<int:id>/components", methods=["GET"])
def user_components_get(id):
    with Session() as session:
        try:
            components = session.get(User, id).components
            return jsonify([component.to_dict() for component in components]), 200
        except Exception as e:
            return jsonify(error=str(e)), 500


@app.route("/components", methods=["GET"])
def components_get():
    with Session() as session:
        try:
            components = session.query(Component).all()
            return jsonify([component.to_dict() for component in components]), 200
        except Exception as e:
            return jsonify(error=str(e)), 500


@app.route("/component", methods=["POST"])
def component_post():
    r = request.get_json()

    for key in ["user_id", "name", "content"]:
        if key not in r:
            return jsonify(error=f"Missing '{key}' key."), 400

    with Session() as session:
        try:
            component = Component(name=r["name"], content=r["content"])
            session.add(component)
            session.flush()

            user_component = UserComponent(
                user_id=r["user_id"], component_id=component.id
            )
            session.add(user_component)
            session.commit()
            return jsonify(component.to_dict()), 200
        except Exception as e:
            session.rollback()
            return jsonify(error=str(e)), 500


@app.route("/component/<int:id>", methods=["GET"])
def component_get(id):
    with Session() as session:
        try:
            component = session.query(Component).filter_by(id=id).first()
            if component is None:
                return jsonify(error=f"Component '{id}' not found."), 404
            return jsonify(component.to_dict()), 200
        except Exception as e:
            return jsonify(error=str(e)), 500


@app.route("/component/<int:id>", methods=["PUT"])
def component_put(id):
    r = request.get_json()

    if "name" not in r or "content" not in r:
        return jsonify(error="Missing required keys: 'name' and 'content'"), 400

    with Session() as session:
        try:
            component = session.get(Component, id)
            if component is None:
                return jsonify(error=f"Component '{id}' not found."), 404
            component.name = r["name"]
            component.content = r["content"]
            session.commit()
            return jsonify(component.to_dict()), 200
        except Exception as e:
            session.rollback()
            return jsonify(error=str(e)), 500


@app.route("/component/<int:id>", methods=["DELETE"])
def component_delete(id):
    with Session() as session:
        try:
            component = session.get(Component, id)
            if component is None:
                return jsonify(error=f"Component '{id}' not found."), 404
            session.delete(component)
            session.commit()
            return jsonify(component.to_dict()), 200
        except Exception as e:
            session.rollback()
            return jsonify(error=str(e)), 500
