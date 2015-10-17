# -*- encoding:utf-8 -*-
from entry import app
from flask import request,jsonify
from flask import render_template
from functools import wraps
import logging

import service.db as db


logger = logging.getLogger(__name__)

sessions = dict()

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
#@utils.func_timer.decorator
def default():
    return render_template("index.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/login.html")
def login_page():
    return render_template("login.html")

@app.route("/trylogin")
@jsonp
def login():
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    session = request.cookies.get("sessionid")
    if session is not None:
        render_template("console.html")

    sql_stmt =  "SELECT * FROM `user` WHERE email = \"%s\" AND pwd = \"%s\" " %(user,passwd)
    result = db.execute(sql_stmt )


    if (len(result)!=0):
        return jsonify({'status':True})
    else:
        return jsonify({'status':False})

