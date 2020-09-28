from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hicaiji.com@mh.hicaiji.com:3306/soul'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'xxx'
db2 = SQLAlchemy(app)
from models import db, Soup


# soul
class Soul(db2.Model):
    __tablename__ = "soul"
    id = db2.Column(db2.Integer, primary_key=True)  # id号(独一无二的)
    title = db2.Column(db2.String(128), nullable=False)
    hits = db2.Column(db2.Integer, nullable=False, default=0)  # 浏览量


soups = Soul.query.all()
for soup in soups:
    s = Soup(content=soup.title, hits=soup.hits)
    db.session.add(s)
db.session.commit()
