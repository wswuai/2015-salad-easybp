# -*- encoding:utf-8 -*-
from entry import app
from flask import request,jsonify,redirect,make_response
from flask import render_template
from functools import wraps
import logging
import os

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
    return render_template("default.html")

@app.route("/richtext.html")
def rich():

    return render_template("richtext.html")

@app.route("/login.html")
def login_page():
    return render_template("login.html")

@app.route("/Registration.html")
def Registration():
    return render_template("Registration.html")

@app.route("/index.html")
def index_html():
    sid = request.cookies.get("sessionId")

    bid = sessions[sid]['info'][0]

    book = db.execute("SELECT * FROM user WHERE id = %s" % str(bid) ) [0][13]

    book = json.loads(book)

    if book is None:
        book = {}

    return render_template("index.html",context=book)

@app.route("/Layout.html")
def layout_html():
    return render_template("Layout.html")

@app.route("/BPreview.html")
def bprewview_html():
    global sessions

    sid = request.cookies.get("sessionId")

    bid = sessions[sid]['info'][0]

    book = db.execute("SELECT * FROM user WHERE id = %s" % str(bid) ) [0][13]

    book = json.loads(book)

    return render_template("BPreview.html",context=book)


import sha
import time

@app.route("/trylogin")
def login():
    global sessions
    user = request.args.get("user")
    passwd = request.args.get("passwd")
    session = request.cookies.get("sessionId")
    if session in sessions.keys():
        #JUMP TO ...
        #return render_template("index.html")
        print sessions
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

    user = request.args['email']
    passwd = request.args['pwd']

    sql_stmt =  "SELECT * FROM `user` WHERE email = \"%s\" AND pwd = \"%s\" " %(user,passwd)
    result = db.execute(sql_stmt )
    print result


    new_ssid = str(sha.sha(str(time.time())).hexdigest())
    sessions[new_ssid] = {"info":result[0]}

    ret = redirect("/index.html")
    ret.set_cookie("sessionId",new_ssid)

    return ret





import json
@app.route("/getBookContent")
@jsonp
def getBookContent():
    global sessions
    sid = request.cookies.get("sessionId")

    bid = sessions[sid]['info'][0]

    book = db.execute("SELECT * FROM user WHERE id = %s" % str(bid) ) [0][13]

    book = json.loads(book)

    return jsonify(book)




@app.route("/setBookContent",methods=['GET','POST'])
def setBookContent():
    global sessions
    sid = request.cookies.get("sessionId")

    bid = sessions[sid]['info'][0]

    print request.form

    book = dict(request.form)

    book = dict( (k,v[0]) for (k,v) in book.items() )

    json_string = json.dumps(book)
    update_stmt =  "UPDATE user SET content = %s WHERE id= %s "

    #db.execute(update_stmt,json_string,bid)

    conn = db.get_conn()

    cur = conn.cursor()

    cur.execute(update_stmt,(json_string,bid))

    conn.commit()

    conn.close()

    return "OK"


@app.route("/sessions")
def sesslist():
   return  str(sessions)


from uploader import Uploader
import re

@app.route('/upload/', methods=['GET', 'POST', 'OPTIONS'])
def upload():
    """UEditor文件上传接口

    config 配置文件
    result 返回结果
    """
    mimetype = 'application/json'
    result = {}
    action = request.args.get('action')

    # 解析JSON格式的配置文件
    with open(os.path.join(app.static_folder, 'ueditor', 'php',
                           'config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}

    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG

    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }

        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, app.static_folder)
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('uploadscrawl'):
        # 涂鸦上传
        fieldName = CONFIG.get('scrawlFieldName')
        config = {
            "pathFormat": CONFIG.get('scrawlPathFormat'),
            "maxSize": CONFIG.get('scrawlMaxSize'),
            "allowFiles": CONFIG.get('scrawlAllowFiles'),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, app.static_folder, 'base64')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('catchimage'):
        config = {
            "pathFormat": CONFIG['catcherPathFormat'],
            "maxSize": CONFIG['catcherMaxSize'],
            "allowFiles": CONFIG['catcherAllowFiles'],
            "oriName": "remote.png"
        }
        fieldName = CONFIG['catcherFieldName']

        if fieldName in request.form:
            # 这里比较奇怪，远程抓图提交的表单名称不是这个
            source = []
        elif '%s[]' % fieldName in request.form:
            # 而是这个
            source = request.form.getlist('%s[]' % fieldName)

        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, app.static_folder, 'remote')
            info = uploader.getFileInfo()
            _list.append({
                'state': info['state'],
                'url': info['url'],
                'original': info['original'],
                'source': imgurl,
            })

        result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
        result['list'] = _list

    else:
        result['state'] = '请求地址出错'

    result = json.dumps(result)

    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            result = '%s(%s)' % (callback, result)
            mimetype = 'application/javascript'
        else:
            result = json.dumps({'state': 'callback参数不合法'})

    res = make_response(result)
    res.mimetype = mimetype
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res
