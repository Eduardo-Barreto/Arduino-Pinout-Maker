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
        self.legend_multiplier = int(names_dict.get("LegendMultiplier"))

    def load_settings(self, sizes_dict):
        connections_dict = sizes_dict.get("Connections")
        names_dict = sizes_dict.get("Names")

        if connections_dict is not None:
            self.connection_radius = int(
                connections_dict.get("Radius", self.connection_radius)
            )
            self.connection_size = int(
                connections_dict.get("Size", self.connection_size)
            )
            self.connection_width = int(
                connections_dict.get("Width", self.connection_width)
            )

        if names_dict is not None:
            self.name_height = int(
                names_dict.get("Height", self.name_height)
            )
            self.name_border = int(
                names_dict.get("Border", self.name_border)
            )
            self.name_border_radius = int(
                names_dict.get("BorderRadius", self.name_border_radius)
            )
            self.font = int(
                names_dict.get("Font", self.font)
            )
            self.legend_multiplier = int(
                names_dict.get("LegendMultiplier", self.legend_multiplier)
            )


class Board:
    def __init__(self, name: str, json_file: str):
        self.name = name
        self.__dict__ = json.load(open(json_file, encoding='utf-8')).get(name)

        standard = self.__dict__.get('Settings')

        self.image_path = standard.get('ImagePath')
        self.font_path = standard.get('FontPath')
        self.colors = standard.get('Colors')
        self.sizes = Sizes(standard.get('Sizes'))

        self.ports = self.__dict__.get('Ports')
        self.connections = []
        self.used_types = []

    def load_settings(self, settings):
        if settings is None:
            return

        self.image_path = settings.get('ImagePath', self.image_path)
        self.font_path = settings.get('FontPath', self.font_path)

        colors = settings.get('Colors', self.colors)

        self.colors['Connections'] = colors.get(
            'Connections', self.colors.get('Connections')
        )

        portTypes = colors.get('PortTypes', self.colors.get('PortTypes'))
        for item, value in portTypes.items():

            standard = self.colors.get('PortTypes').get(
                item,
                {"Background": None, "Text": None}
            )

            bg = value.get('Background', standard.get('Background'))
            text = value.get('Text', standard.get('Text'))
            self.colors['PortTypes'].update(
                {item: {'Background': bg, 'Text': text}}
            )

        sizes = settings.get('Sizes', self.sizes.__dict__)
        self.sizes.load_settings(sizes)
