import os
from uuid import uuid4
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    Float,
    Date,
    DateTime,
    null,
    ARRAY,
    text
)
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

#### Local Development

DATABASE_NAME = os.getenv("DB_NAME","stagemanager")
DATABASE_USER = os.getenv("DB_USER","stagemanager_user")
DATABASE_PASSWORD = os.getenv("DB_PASS",'stage')
DATABASE_HOST = os.getenv('DB_HOST',"localhost:5432")
DATABASE_PATH = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

db = SQLAlchemy()

def setup_db(app, path=DATABASE_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

class StageManagerModel(db.Model):
    __abstract__  = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Venue(StageManagerModel):
    __tablename__ = "venues"

    id = Column(UUID(as_uuid=True),primary_key=True,server_default=uuid4)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    style = Column(String, nullable=False)
    shows = db.relationship('Show',backref='venue')

    def __init__(self, name, capacity, style):
        self.id = id
        self.name = name
        self.capacity = capacity
        self.style = style    

    def format(self):
        return {
            "id":self.id,
            "name":self.name,
            "capacity":self.capacity,
            "style":self.style
        }  

class Show(StageManagerModel):
    __tablename__ = "shows"

    id = Column(UUID(as_uuid=True),primary_key=True,server_default=uuid4)
    name = Column(String, nullable=False)
    rehersals_begin = Column(Date)
    previews_begin = Column(Date)
    opening_night = Column(Date)
    closing_night = Column(Date)
    show_type = Column(String, nullable=False)
    venue_id = Column(UUID(as_uuid=True), ForeignKey('venues.id'))

    def __init__(self, name, show_type):
        self.id = id
        self.name = name
        self.show_type = show_type

class Person(StageManagerModel):
    __tablename__ = "persons"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid4())
    fist_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    billed_as = Column(String, nullable=False)
    position = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    union_affiliation = Column(String)
    group_affiliation = Column(String)

    def __init__(self, id, position, first_name, last_name, billed_as=None):
        self.id = id
        self.position = position
        self.first_name = first_name
        self.last_name = last_name
        if billed_as:
            self.billed_as = billed_as
        else:
            self.billed_as = self.first_name + self.last_name
    



