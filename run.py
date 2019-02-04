from app import app

if __name__ == '__main__':
    app.run(host="localhost", port=59001, debug=True, threaded=True)