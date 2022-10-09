import json


class Connection:
    def __init__(self, connection_dict):
        self.port = list(connection_dict.keys())[0]
        connection_dict = connection_dict.get(self.port)

        self.name = connection_dict.get('Name')
        self.in_out = connection_dict.get('InOut')
        self.type = connection_dict.get('Type')


class Sizes:
    def __init__(self, sizes_dict):
        self.__dict__ = sizes_dict

        connections_dict = self.__dict__.get("Connections")
        names_dict = self.__dict__.get("Names")

        self.connection_radius = int(connections_dict.get("Radius"))
        self.connection_size = int(connections_dict.get("Size"))
        self.connection_width = int(connections_dict.get("Width"))

        self.name_height = int(names_dict.get("Height"))
        self.name_border = int(names_dict.get("Border"))
        self.name_border_radius = int(names_dict.get("BorderRadius"))
        self.font = int(names_dict.get("Font"))


class Board:
    def __init__(self, name: str, json_file: str):
        self.name = name
        self.__dict__ = json.load(open(json_file, encoding='utf-8')).get(name)

        self.settings = self.__dict__.get('Settings')
        self.load_settings(self.settings)

        self.ports = self.__dict__.get('Ports')
        self.connections = []

    def load_settings(self, settings):
        if settings is None:
            self.load_settings(self.settings)

        self.image_path = settings.get('ImagePath')
        self.font_path = settings.get('FontPath')

        self.colors = settings.get('Colors')
        self.sizes = Sizes(settings.get('Sizes'))
