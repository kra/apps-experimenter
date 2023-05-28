from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/twiml', methods=['POST'])
def streams_twiml():
    print("this is a log message from webserver")
    return render_template('streams.xml')
