# -*- encoding:utf-8 -*-
from entry import app
from flask import request
from flask import render_template
import logging

import service.db as db


logger = logging.getLogger(__name__)

sessions = dict()

def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args).encode("utf-8")



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

@app.route("/login")
def login():
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    session = request.cookies.get("sessionid")
    if session is not None:
        render_template("console.html")

    result = db.execute("SELECT * FROM `user` WHERE email = %s AND pwd = %s " %(user,passwd) )

    if (len(result)!=0):
        return "OK"
    else:
        return "Failed"

