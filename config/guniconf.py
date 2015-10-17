#import os

bind='0.0.0.0:5678'

workers=16

backlog=2048

worker_class="gevent" #sync, gevent,meinheld

debug=False

#proc_name='gunicorn.pid'

pidfile='log/esearchweb.pid'

loglevel='info'

accesslog='log/server.log'

errorlog='log/error.log'

#daemon=False
daemon=True
