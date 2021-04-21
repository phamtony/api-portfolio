from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class ModelFunc():
    def __init__(self):
        super().__init__()

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class General(db.Model, ModelFunc):
    __tablename__ = "general"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    email = db.Column(db.String(100))
    github = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))

    experience = relationship("Experience", back_populates="general")
    education = relationship("Education", back_populates="general")
    project = relationship("Project", back_populates="general")
    about = relationship("About", uselist=False, back_populates="general")
    skills = relationship("Skills", uselist=False, back_populates="general")


class About(db.Model, ModelFunc):
    __tablename__ = "about"
    id = db.Column(db.Integer, primary_key=True)
    intro = db.Column(db.String(1000))
    image = db.Column(db.String(250))
    section_one = db.Column(db.String(500))
    skills_work = db.Column(db.String(250))
    section_two = db.Column(db.String(500))
    skills_goto = db.Column(db.String(250))

    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    general = relationship("General", back_populates="about")


class Experience(db.Model, ModelFunc):
    __tablename__ = "experience"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    position = db.Column(db.String(100))
    time = db.Column(db.String(100))
    link = db.Column(db.String(250))
    description = db.Column(db.String(1000))

    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    general = relationship("General", back_populates="experience")


class Education(db.Model, ModelFunc):
    __tablename__ = "education"
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(150))
    time = db.Column(db.String(100))
    degree = db.Column(db.String(250))

    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    general = relationship("General", back_populates="education")


class Skills(db.Model, ModelFunc):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(500))
    framework_library = db.Column(db.String(500))
    database = db.Column(db.String(500))
    misc = db.Column(db.String(500))

    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    general = relationship("General", back_populates="skills")


class Project(db.Model, ModelFunc):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    link = db.Column(db.String(250))
    github_link = db.Column(db.String(250))
    screenshot = db.Column(db.String(250))
    description = db.Column(db.String(500))
    tech_list = db.Column(db.String(250))

    # Create Foreign Key, "general.id" the users refers to the tablename of General.
    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    # Create reference to the General object, the "project" refers to the project property in the General class.
    general = relationship("General", back_populates="project")
