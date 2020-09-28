from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:// '# 自己的数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'xxx'
db = SQLAlchemy(app)

# 用户表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    openid = db.Column(db.String(256), nullable=False, unique=True)  # openid
    username = db.Column(db.String(256))  # username
    avatar = db.Column(db.String(256))  # 头像
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    soups = db.relationship("Soup", secondary="user_soup", backref="users")  # 用户与鸡汤的关系 多对多


# 用户表-鸡汤表中间表
class UserSoup(db.Model):
    __tablename__ = "user_soup"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 用户的id
    soup_id = db.Column(db.Integer, db.ForeignKey("soup.id"))  # 鸡汤的id


# 鸡汤表
class Soup(db.Model):
    __tablename__ = "soup"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    content = db.Column(db.String(1024), nullable=False)  # 文字
    hits = db.Column(db.Integer, nullable=False, default=0)  # 浏览量


if __name__ == "__main__":
    db.create_all()
    # db.drop_all()
