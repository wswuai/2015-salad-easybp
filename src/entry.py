from flask import Flask



app = Flask(__name__,static_url_path='')
app.config.from_object('config.dev.TestingConfig')

import views
