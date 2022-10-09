import json

from draw import Draw
from board import Board, Connection

user = json.load(open('../examples/styles.json', encoding='utf-8'))
board = user.get('Board')
settings = user.get('Settings')
connections = user.get('Connections')

arduino = Board(board, '../data/boards.json')
arduino.load_settings(settings)

drawing = Draw(arduino)

for port, details in connections.items():
    connection = Connection({port: details})
    drawing.port(connection)

drawing.color_legend()
drawing.img.save('../examples/styles.jpg')
