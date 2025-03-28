from sqlalchemy.orm import relationship
from flask_login import UserMixin

from extensions import db


class General(db.Model, UserMixin):
    __tablename__ = "general"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(200))
    occupation = db.Column(db.String(100))
    email = db.Column(db.String(100))
    github = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))
    user_intro = db.Column(db.String(3000))
    api_key = db.Column(db.String(100))

    experience = relationship("Experience", back_populates="general")
    education = relationship("Education", back_populates="general")
    project = relationship("Project", back_populates="general")
    about = relationship("About", uselist=False, back_populates="general")
    skills = relationship("Skills", uselist=False, back_populates="general")

    def __repr__(self):
        return "<General(name='%s', occupation='%s', email='%s', github='%s', linkedin='%s', user_intro='%s')>" % (self.name, self.occupation, self.email, self.github, self.linkedin, self.user_intro)

    @property
    def serialized(self):
        return {
            "name": self.name,
            "occupation": self.occupation,
            "email": self.email,
            "github": self.github,
            "linkedin": self.linkedin,
            "user_intro": self.user_intro,
        }


class About(db.Model):
    __tablename__ = "about"
    id = db.Column(db.Integer, primary_key=True)
    intro = db.Column(db.String(3000))
    image = db.Column(db.String(250))

    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    general = relationship("General", back_populates="about")

    def __repr__(self):
        return "<About(intro='%s', image='%s')>" % (self.intro, self.image)

    @property
    def serialized(self):
        return {
            "intro": self.intro,
            "image": self.image,
        }


class Experience(db.Model):
    __tablename__ = "experience"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    position = db.Column(db.String(100))
    time = db.Column(db.String(100))
    link = db.Column(db.String(250))
    description = db.Column(db.String(2500))
    order_exp = db.Column(db.Integer)

    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    general = relationship("General", back_populates="experience")

    def __repr__(self):
        return "<Experience(id='%s', name='%s', position='%s', time='%s', link='%s', description='%s')>" % (self.id, self.name, self.position, self.time, self.link, self.description)

    @property
    def serialized(self):
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position,
            "time": self.time,
            "link": self.link,
            "description": self.description,
        }


class Education(db.Model):
    __tablename__ = "education"
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(150))
    time = db.Column(db.String(100))
    degree = db.Column(db.String(250))
    order_ed = db.Column(db.Integer)

    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    general = relationship("General", back_populates="education")

    def __repr__(self):
        return "<Education(id='%s', school='%s', time='%s', degree='%s')>" % (self.id, self.school, self.time, self.degree)

    @property
    def serialized(self):
        return {
            "id": self.id,
            "school": self.school,
            "time": self.time,
            "degree": self.degree,
        }


class Skills(db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(500))
    framework_library = db.Column(db.String(500))
    database = db.Column(db.String(500))
    misc = db.Column(db.String(500))

    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    general = relationship("General", back_populates="skills")

    def __repr__(self):
        return "<Skills(language='%s', framework_library='%s', database='%s', misc='%s')>" % (self.language, self.framework_library, self.database, self.misc)

    @property
    def serialized(self):
        return {
            "language": self.language,
            "framework_library": self.framework_library,
            "database": self.database,
            "misc": self.misc,
        }


class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    link = db.Column(db.String(250))
    github_link = db.Column(db.String(250))
    screenshot = db.Column(db.String(250))
    description = db.Column(db.String(1500))
    tech_list = db.Column(db.String(250))
    order_project = db.Column(db.Integer)

    # Create Foreign Key, "general.id" the users refers to the tablename of General.
    general_id = db.Column(db.Integer, db.ForeignKey("general.id"))
    # Create reference to the General object, the "project" refers to the project property in the General class.
    general = relationship("General", back_populates="project")

    def __repr__(self):
        return "<Project(id='%s', name='%s', link='%s', github_link='%s', screenshot='%s', description='%s', tech_list='%s')>" % (self.id, self.name, self.link, self.github_link, self.screenshot, self.description, self.tech_list)

    @property
    def serialized(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "github_link": self.github_link,
            "screenshot": self.screenshot,
            "description": self.description,
            "tech_list": self.tech_list,
        }
