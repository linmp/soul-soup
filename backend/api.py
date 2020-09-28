import time

import redis
import requests
from flask import request, jsonify
from models import app
from models import db, User, Soup, UserSoup
from sqlalchemy import func

limit = 10
qq_appid = 'xx'
qq_secret = 'xx'
wx_appid = 'xx'
wx_secret = 'xx'


redis_store = redis.Redis(host='x.x.com', port=6379, password="xx", db=4,
                          decode_responses=True)  # 操作的redis配置


# qq登录 后台去获取登录信息 ，小程序传入请求的lg_code去获取用户的openid //
@app.route('/qq/login')
def qq_login():
    lg_code = request.args.get('lg_code')
    url = f"https://api.q.qq.com/sns/jscode2session?appid={qq_appid}&secret={qq_secret}&js_code={lg_code}&grant_type=authorization_code"
    rq = requests.get(url)
    rq_json = rq.json()
    print(rq_json)

    if rq_json.get('errcode'):
        data = {"error": rq_json.get('errmsg')}
        data = jsonify(data)
        return data
    else:
        data = jsonify({"openid": rq_json.get('openid')})

        openid = rq_json.get('openid')
        user = User.query.filter_by(openid=openid).first()
        # 注册
        if user is None:

            user = User(openid=openid)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

        return data


# wx登录 后台去获取登录信息 ，小程序传入请求的lg_code去获取用户的openid //
@app.route('/wx/login')
def wx_login():
    lg_code = request.args.get('lg_code')
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={wx_appid}&secret={wx_secret}&js_code={lg_code}&grant_type=authorization_code"
    rq = requests.get(url)
    rq_json = rq.json()
    print(rq_json)

    if rq_json.get('errcode'):
        data = {"error": rq_json.get('errmsg')}
        data = jsonify(data)
        return data
    else:
        data = jsonify({"openid": rq_json.get('openid')})
        openid = rq_json.get('openid')
        user = User.query.filter_by(openid=openid).first()
        # 注册
        if user is None:

            user = User(openid=openid)
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

        return data


# 字节tt登录 后台去获取登录信息 ，小程序传入请求的lg_code去获取用户的openid //
@app.route('/tt/login')
def tt_login():
    """
    请求获得用户的openid
    属性	类型	默认值	必填	说明
    appid	string		是	小程序 appId
    secret	string		是	小程序 appSecret
    js_code	string		是	登录时获取的 code
    grant_type	string		是	授权类型，此处只需填写 authorization_code
    :return:
    返回的 JSON 数据包
    属性	类型	说明
    openid	string	用户唯一标识
    session_key	string	会话密钥
    unionid	string	用户在开放平台的唯一标识符，在满足 UnionID 下发条件的情况下会返回，详见 UnionID 机制说明。
    errcode	number	错误码
    errmsg	string	错误信息
    """
    lg_code = request.args.get('lg_code')
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={wx_appid}&secret={wx_secret}&js_code={lg_code}&grant_type=authorization_code"
    rq = requests.get(url)
    rq_json = rq.json()
    print(rq_json)

    if rq_json.get('errcode'):
        data = {"error": rq_json.get('errmsg')}
        data = jsonify(data)
        return data
    else:
        data = jsonify({"openid": rq_json.get('openid')})
        return data


# 更新用户的信息 openid 昵称 头像链接  注册新用户 判断用户状态
@app.route('/update', methods=["POST"])
def update():
    req_json = request.get_json()
    openid = req_json.get("openid")
    username = req_json.get("username")
    avatar = req_json.get("avatar")

    if openid is None:
        return jsonify({'error': "error no openid"})

    user = User.query.filter_by(openid=openid).first()

    # 注册
    if user is None:

        user = User(openid=openid, username=username, avatar=avatar)

        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(msg="add user success", code=200)

        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify(code=400, msg="add user error")

    # 更新数据
    else:
        user.username = username
        user.avatar = avatar

        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(msg="数据库更新数据完成")
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify(re_code=400, msg="数据库更新数据异常")


# 查看鸡汤
@app.route("/soup", methods=["GET"])
def get_soup():
    soups = db.session.query(Soup).order_by(func.rand()).limit(limit)
    payload = []
    for soup in soups:
        soup.hits += 1
        db.session.add(soup)

        payload.append({
            "id": soup.id,
            "content": soup.content,
            "hits": soup.hits
        })
    try:
        db.session.commit()
        return jsonify(code=200, msg="查询成功", data=payload)

    except Exception as e:
        print(e)
        db.session.rollback()
    return jsonify(code=200, msg="成功", data=payload)


# 收藏 需要openid
@app.route("/collect", methods=["POST"])
def collect_soup():
    print(request)
    req_json = request.get_json()
    soup_id = req_json.get("soup_id")
    openid = req_json.get("openid")
    if not all([soup_id, openid]):
        return jsonify(code=4000, msg="参数不完整")

    user = User.query.filter_by(openid=openid).first()
    if user is None:
        return jsonify(code=4001, msg="用户不存在")

    soup = Soup.query.get(soup_id)
    if soup is None:
        return jsonify(code=4002, msg="鸡汤不存在")

    try:
        user.soups.append(soup)
        db.session.add(user)
        db.session.commit()
        return jsonify(code=200, msg="收藏成功")
    except Exception as e:
        print(e)
        return jsonify(code=4003, msg="收藏失败")


# 取消收藏 需要openid
@app.route("/collect/delete", methods=["POST"])
def delete_collect_soup():
    print(request.get_json())
    time.sleep(1)
    req_json = request.get_json()
    soup_id = req_json.get("soup_id")
    openid = req_json.get("openid")

    if not all([soup_id, openid]):
        return jsonify(code=4000, msg="参数不完整")

    user = User.query.filter_by(openid=openid).first()
    if user is None:
        return jsonify(code=4001, msg="用户不存在")

    soup = Soup.query.get(soup_id)
    if soup is None:
        return jsonify(code=4002, msg="鸡汤不存在")

    user_soup = UserSoup.query.filter_by(soup_id=soup_id, user_id=user.id).delete()
    try:
        db.session.commit()
        return jsonify(code=200, msg="操作删除卡片成功", delete_amount=user_soup)
    except Exception as e:
        print(e)
        return jsonify(code=4003, msg="操作删除卡片失败")


# 查看我的收藏 需要openid
@app.route("/collects", methods=["GET"])
def check_my_collect():
    req_args = request.args
    openid = req_args.get("openid")
    page = req_args.get("page")
    if not all([page, openid]):
        return jsonify(code=4000, msg="参数不完整")
    page = int(page)
    user = User.query.filter_by(openid=openid).first()
    if user is None:
        return jsonify(code=4001, msg="用户不存在")

    soups = user.soups
    # soups = Soup.query.filter_by()
    payload = []
    for soup in soups:
        soup.hits += 1
        db.session.add(soup)
        payload.append({
            "id": soup.id,
            "content": soup.content,
            "hits": soup.hits
        })
    return jsonify(code=200, msg="查询成功", data=payload)
