from flask import Flask
from flask_socketio import SocketIO
import datetime
from translator import translate_notation

x = datetime.datetime.now()

app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")

# SocketIO to handle new connections
# Prints for every new connection
@socket_io.on('connect')
def handle_connect():
    print('new connection')

# Will print the sent argument amd semd back the current time
@socket_io.on('to-server')
def handle_to_server(arg):
    print(f'new to-server event: {arg}')
    message = input('Enter message: ')
    socket_io.emit('from-server', message)

# @app.route('/data')
# def data():
#     return {
#         'Name': "geek",
#         'Age': '21',
#         'Date': x,
#         'Programming': 'Python'
#     }

# def getUserInput():
#     previous = input("Enter previous position: ")
#     current = input("Enter next position: ")
#     return translate_notation(previous, current)

# @app.route('/moves', methods=['GET'])
# def moves():
#     prevX, prevY, nextX, nextY = getUserInput()
#     return {
#         'prevX': prevX,
#         'prevY': prevY,
#         'nextX': nextX,
#         'nextY': nextY
#         }

if __name__ == '__main__':
    socket_io.run(app, port=5000)
