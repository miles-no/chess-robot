from flask import Flask
import datetime

x = datetime.datetime.now()

app = Flask(__name__)

@app.route('/data')
def data():
    return {
        'Name': "geek",
        'Age': '21',
        'Date': x,
        'Programming': 'Python'
    }


if __name__ == '__main__':
    app.run(debug=True)