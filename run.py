# Template file for run.py, which is used to start the development werkzeug server

from autoapi_testapp.app import app



# Label server as development
app.env = 'development'

# Enable better exceptions and hot reloading
DEBUG = True
USE_RELOADER = False

# Sever ip:port.  Use HOST = 0.0.0.0 for access outside dev machine
HOST = "0.0.0.0"
PORT = 5000

# Enable server to use multiple threads
THREADED = True

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG, threaded=THREADED, use_reloader=USE_RELOADER)

