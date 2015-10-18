# -*- encoding:utf-8 -*-
from entry import app
from flask import request,jsonify,redirect,send_from_directory
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

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/login.html")
def login_page():
    return render_template("login.html")

@app.route("/Registration.html")
def Registration():
    return render_template("Registration.html")

@app.route("/index.html")
def index_html():
    return render_template("index.html")

@app.route("/Layout.html")
def layout_html():
    return render_template("Layout.html")



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

    ret = redirect("/")
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



@app.route('/ueditor')
def ueditor_init():
    return render_template('ueditor.html')


@app.route('/ueditor/config')
def ueditor_config():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'ueditor/config.json', mimetype='text/html')



from werkzeug.utils import secure_filename
@app.route('/ueditor/uploadimage',methods=['POST'])
def ueditor_uploadimage():
    app.config['UPLOAD_FOLDER']=os.path.join(app.root_path,'static/upload/image')
    file = request.files['upfile']
    filename=secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    return jsonify(state='SUCCESS',
                   url="/static/upload/image/"+filename,
                   title=filename)



