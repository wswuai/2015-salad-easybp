# -*- encoding:utf-8 -*-
from entry import app
from flask import request,jsonify,abort
from flask import render_template
from functools import wraps
import logging

import service.db as db


logger = logging.getLogger(__name__)

sessions = {}

def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args).encode("utf-8")


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function



@app.route("/")
def default():
    return render_template("index.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/login.html")
def login_page():
    return render_template("login.html")


import sha
import time

@app.route("/trylogin")
@jsonp
def login():
    global sessions
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    session = request.cookies.get("sessionId")
    if session in sessions.keys():
        #JUMP TO ...
        #return render_template("index.html")
        return "Logined :: " + str(session)

    sql_stmt =  "SELECT * FROM `user` WHERE email = \"%s\" AND pwd = \"%s\" " %(user,passwd)
    result = db.execute(sql_stmt )

    if (len(result)!=0):
        new_ssid = str(sha.sha(str(time.time())).hexdigest())
        print new_ssid
        ret = jsonify({'status':True})
        ret.set_cookie("sessionId",new_ssid)
        sessions[new_ssid] = {"info":result[0]}
        return ret
    else:
        return jsonify({'status':False})

@app.route("/register")
def register():
    dic = request.args
    db.insert_into_table("user",dic)
    return "OK"


import json
@app.route("/getBookContent")
def getBookContent():
    global sessions
    sid = request.cookies.get("sessionId")

    bid = sessions[sid]['info'][0]

    book = db.execute("SELECT * FROM user WHERE id = %s" % str(bid) ) [0][13]

    book = json.loads(book)

    return jsonify(book)


@app.route("/setBookContent")
def setBookContent():
    global sessions
    sid = request.cookies.get("sessionId")

    bid = sessions[sid]['info'][0]

    content = request.args.get("content")

    content = json.loads(content)

    category = request.args.get("category")

    if None in [bid,content,category]:
        abort(400)

    book = db.execute("SELECT * FROM user WHERE id = %s " % str(bid) ) [0][13]

    book = json.loads(book)

    book[category] = content

    update_stmt =  "UPDATE user SET content = '%s' WHERE id=%s " % (json.dumps(book),bid)

    db.execute(update_stmt)

    return "OK"


@app.route("/sessions")
def sesslist():
   return  str(sessions)
