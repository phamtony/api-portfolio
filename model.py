from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class General(db.Model):
    __tablename__ = "general"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    email = db.Column(db.String(100))
    github = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))

    experience = relationship("Experience", back_populates="general")
    education = relationship("Education", back_populates="general")


class About(db.Model):
    __tablename__ = "about"
    id = db.Column(db.Integer, primary_key=True)
    intro = db.Column(db.String(1000))
    image = db.Column(db.String(250))
    section_one = db.Column(db.String(500))
    skills_work = db.Column(db.String(250))
    section_two = db.Column(db.String(500))
    skills_goto = db.Column(db.String(250))


class Experience(db.Model):
    __tablename__ = "experience"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    position = db.Column(db.String(100))
    time = db.Column(db.String(100))
    link = db.Column(db.String(250))
    description = db.Column(db.String(1000))

    # Create Foreign Key, "general.id" the users refers to the tablename of General.
    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    # Create reference to the General object, the "experience" refers to the experience property in the General class.
    general = relationship("General", back_populates="experience")


class Education(db.Model):
    __tablename__ = "education"
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(150))
    time = db.Column(db.String(100))
    degree = db.Column(db.String(250))

    # Create Foreign Key, "general.id" the users refers to the tablename of General.
    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    # Create reference to the General object, the "experience" refers to the experience property in the General class.
    general = relationship("General", back_populates="education")
