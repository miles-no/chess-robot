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

def getUserInput():
    prevX = int(input('Previous X: '))
    prevY = int(input('Previous Y: '))
    nextX = int(input('Next X: '))
    nextY = int(input('Next Y: '))
    return prevX, prevY, nextX, nextY

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