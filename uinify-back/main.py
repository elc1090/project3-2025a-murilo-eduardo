from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import event

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

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
    title = Column(String(256), nullable=False)
    description = Column(Text(), nullable=True)
    framework = Column(String(50), nullable=False)  # vue, react, html/css
    category = Column(String(50), nullable=False)   # ui, forms, navigation, cards, data, layout
    tags = Column(Text(), nullable=True)            # Separate tags with commas
    inputType = Column(String(50), nullable=False)  # html, vue
    includeTailwind = Column(Boolean, nullable=False, default=False)
    code = Column(Text(), nullable=False)           # actual content

    def __repr__(self):
        return f"<Component(title='{self.title}', framework='{self.framework}', category='{self.category}')>"

    def to_dict(self):
        # Convert tags string back to list for frontend compatibility
        tags_list = []
        if self.tags:
            tags_list = [tag.strip() for tag in self.tags.split(",") if tag.strip()]

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "framework": self.framework,
            "category": self.category,
            "tags": tags_list,
            "inputType": self.inputType,
            "includeTailwind": self.includeTailwind,
            "code": self.code
        }


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
    component = relationship("Component")

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


@app.route("/login", methods=["POST"])
def login():
    r = request.get_json()

    for key in ["username", "password"]:
        if key not in r:
            return jsonify(error=f"Missing '{key}' key."), 400

    with Session() as session:
        try:
            # Check if user exists by username
            existing_user = session.query(User).filter_by(username=r["username"]).first()

            if existing_user is None:
                # Username doesn't exist, create new user
                new_user = User(username=r["username"], password=r["password"])
                session.add(new_user)
                session.commit()
                return jsonify(new_user.to_dict()), 200
            else:
                # Username exists, validate password
                if existing_user.password == r["password"]:
                    return jsonify(existing_user.to_dict()), 200
                else:
                    return jsonify(error="Invalid password."), 401

        except Exception as e:
            session.rollback()
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
            user = session.get(User, id)
            if user is None:
                return jsonify(error=f"User '{id}' not found."), 404

            # Get the actual Component objects through the UserComponent relationship
            user_components = user.components  # This returns UserComponent objects
            components = [uc.component for uc in user_components]  # Get the actual Component objects
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

    required_keys = ["user_id", "title", "framework", "category", "inputType", "code"]
    for key in required_keys:
        if key not in r:
            return jsonify(error=f"Missing '{key}' key."), 400

    with Session() as session:
        try:
            # Handle tags - convert list to comma-separated string if needed
            tags = r.get("tags", "")
            if isinstance(tags, list):
                tags = ", ".join(tags)

            component = Component(
                title=r["title"],
                description=r.get("description", ""),
                framework=r["framework"],
                category=r["category"],
                tags=tags,
                inputType=r["inputType"],
                includeTailwind=r.get("includeTailwind", False),
                code=r["code"]
            )
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

    required_keys = ["title", "framework", "category", "inputType", "code"]
    for key in required_keys:
        if key not in r:
            return jsonify(error=f"Missing '{key}' key."), 400

    with Session() as session:
        try:
            component = session.get(Component, id)
            if component is None:
                return jsonify(error=f"Component '{id}' not found."), 404

            # Handle tags - convert list to comma-separated string if needed
            tags = r.get("tags", "")
            if isinstance(tags, list):
                tags = ", ".join(tags)

            # Update all fields
            component.title = r["title"]
            component.description = r.get("description", "")
            component.framework = r["framework"]
            component.category = r["category"]
            component.tags = tags
            component.inputType = r["inputType"]
            component.includeTailwind = r.get("includeTailwind", False)
            component.code = r["code"]

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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
