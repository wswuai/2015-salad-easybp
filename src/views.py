# -*- encoding:utf-8 -*-
from entry import app
from flask import request
from flask import render_template
from flask import send_from_directory
import logging


logger = logging.getLogger(__name__)


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

#@app.route("/<path:path>")
#def st(path):
#    print path
#    send_from_directory('*',"../static" + path)

