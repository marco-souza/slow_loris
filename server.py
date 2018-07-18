from flask import Flask
app = Flask(__name__)

conn_count = 0

@app.route("/")
def hello():
    global conn_count
    conn_count+=1
    print("Connections made: {}".format(conn_count))
    return "Hello World!"