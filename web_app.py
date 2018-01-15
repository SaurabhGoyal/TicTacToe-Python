import sys

from web_app.app import app


if __name__ == '__main__':
    host, port = (sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1:5000').split(':')
    app.run(debug=True, host=host, port=int(port))
