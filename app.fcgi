#!/home/www/bqlatastaq.com/env/bin/python 
import sys
sys.path.insert(0, '/home/www/bqlatastaq.com/env/lib/python3.8/site-packages')

from flup.server.fcgi import WSGIServer
from app import create_app


# Removes the /app.fcgi/ from the urls
class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)


app = create_app()
app = ScriptNameStripper(app)

WSGIServer(app).run()