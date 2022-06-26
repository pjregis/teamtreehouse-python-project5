from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('Title', db.String())
    date = db.Column('Created', db.DateTime, default=datetime.datetime.now)
    description = db.Column('Description', db.Text)
    skills_practiced = db.Column('Skills', db.Text)
    github_url = db.Column('GitHub', db.String())

    def __repr__(self):
        return f'''<Project Title: {self.title} Created: {self.date} 
                    Description: {self.description} Skills: {self.skills_practiced}
                    GitHub: {self.github_url}
                    >'''
