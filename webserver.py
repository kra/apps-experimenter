from flask import Flask
from flask import render_template

app = Flask(__name__)


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
@app.route('/twiml', methods=['POST'])
def streams_twiml():
    print("this is a log message")
    return render_template('streams.xml')
=======
@app.route("/")
<<<<<<< HEAD
def hello_world():
    return render_template("index.html")
>>>>>>> 9ff59a8 (foo)
=======
=======
@app.route('/twiml', methods=['POST'])
>>>>>>> df26aaa (foo)
=======
@app.route('/twiml', methods=['POST'])
>>>>>>> df26aaa (foo)
def streams_twiml():
    return render_template('streams.xml')
>>>>>>> 459fdf4 (foo)
=======
@app.route("/")
<<<<<<< HEAD
def hello_world():
    return render_template("index.html")
>>>>>>> 9ff59a8 (foo)
=======
def streams_twiml():
    return render_template('streams.xml')
>>>>>>> 459fdf4 (foo)
