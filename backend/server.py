from flask import Flask
import datetime
from translator import translate_notation

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

def getUserInput():
    previous = input("Enter previous position: ")
    current = input("Enter next position: ")
    return translate_notation(previous, current)

@app.route('/moves', methods=['GET'])
def moves():
    prevX, prevY, nextX, nextY = getUserInput()
    return {
        'prevX': prevX,
        'prevY': prevY,
        'nextX': nextX,
        'nextY': nextY
        }

if __name__ == '__main__':
    app.run(debug=True)