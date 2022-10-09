from PIL import Image
import json

import draw

my_ports = json.load(open('./data/example.json'))
board = my_ports.get('Board')


arduino_path = f'./data/Arduino{board}.jpg'

# Load the json file
arduino_ports = json.load(open('./data/ports.json'))
arduino_ports = arduino_ports.get(board)


with Image.open(arduino_path) as img:

    for port, details in my_ports.get('Ports').items():
        draw.all_port(img, port, details.get('Name'), details.get('InOut'), details.get('Type'), arduino_ports)

    img.show()
