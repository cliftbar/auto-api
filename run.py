from autoapi_testapp.app import app


# Label server as development
app.env = 'development'

# Enable better exceptions and hot reloading
DEBUG: bool = True
USE_RELOADER: bool = False

# Sever ip:port.  Use HOST = 0.0.0.0 for access outside dev machine
HOST: str = "0.0.0.0"
PORT: int = 5001

# Enable server to use multiple threads
THREADED: bool = True

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG, threaded=THREADED, use_reloader=USE_RELOADER)

