from PIL import Image, ImageDraw, ImageFont
from board import Board, Connection


class Draw:
    def __init__(self, board: Board):
        self.board = board
        self.img = Image.open(self.board.image_path)
        self.colors = self.board.colors
        self.sizes = self.board.sizes
        self.ports = self.board.ports
        self.font = ImageFont.truetype(self.board.font_path, self.sizes.font)

    def right_arrow(self, x, y, connection_color, draw):
        draw.line(
            (
                x-self.sizes.connection_size*0.6,
                y,
                x-self.sizes.connection_size*0.6-10,
                y-10
            ),
            fill=connection_color,
            width=self.sizes.connection_width
        )
        draw.line(
            (
                x-self.sizes.connection_size*0.6,
                y,
                x-self.sizes.connection_size*0.6-10,
                y+10
            ),
            fill=connection_color,
            width=self.sizes.connection_width
        )

    def left_arrow(self, x, y, connection_color, draw):
        draw.line(
            (
                x-self.sizes.connection_size*0.6,
                y,
                x-self.sizes.connection_size*0.6+10,
                y-10
            ),
            fill=connection_color,
            width=self.sizes.connection_width
        )
        draw.line(
            (
                x-self.sizes.connection_size*0.6,
                y,
                x-self.sizes.connection_size*0.6+10,
                y+10
            ),
            fill=connection_color,
            width=self.sizes.connection_width
        )

    def connection(self, connection_to_draw: Connection) -> None:
        '''
        Desenha a conexão

        Parâmetros:
        ----------
        connection_to_draw: Connection
            Conexão a ser desenhada
        '''
        port_position = self.ports.get(connection_to_draw.port)
        x, y = int(port_position.get('x')), int(port_position.get('y'))
        connection_color = tuple(self.board.colors.get('Connections'))

        right_side = x > self.img.width/2

        if right_side:
            self.sizes.connection_size = -abs(self.sizes.connection_size)

            if connection_to_draw.in_out == "Input":
                connection_to_draw.in_out = "Output"
            elif connection_to_draw.in_out == "Output":
                connection_to_draw.in_out = "Input"

        else:
            self.sizes.connection_size = abs(self.sizes.connection_size)

        draw = ImageDraw.Draw(self.img)

        draw.ellipse(
            (
                x - self.sizes.connection_radius,
                y - self.sizes.connection_radius,
                x + self.sizes.connection_radius,
                y + self.sizes.connection_radius
            ),
            fill=connection_color
        )

        draw.line(
            (x, y, x-self.sizes.connection_size, y),
            fill=connection_color,
            width=self.sizes.connection_width
        )

        if connection_to_draw.in_out == "Input":
            self.right_arrow(x, y, connection_color, draw)

        elif connection_to_draw.in_out == "Output":
            self.left_arrow(x, y, connection_color, draw)

        elif connection_to_draw.in_out == "Input_Output":
            self.left_arrow(x-15, y, connection_color, draw)
            self.right_arrow(x+15, y, connection_color, draw)

        elif connection_to_draw.in_out == "InputPullup":

            if right_side:
                self.left_arrow(x, y, connection_color, draw)
            else:
                self.right_arrow(x, y, connection_color, draw)

            init_x = x - self.sizes.connection_radius
            init_y = y - self.sizes.connection_radius
            end_x = x + self.sizes.connection_radius
            end_y = y + self.sizes.connection_radius

            draw.ellipse(
                (
                    (init_x)-self.sizes.connection_size*0.55,
                    (init_y),
                    (end_x)-self.sizes.connection_size*0.55,
                    (end_y)
                ),
                fill=connection_color
            )

    def name(self, connection_to_draw: Connection):
        '''
        Desenha o nome da conexão

        Parâmetros:
        ----------
        connection_to_draw: Connection
            Conexão a ser desenhada
        '''

        port_position = self.ports.get(connection_to_draw.port)
        x, y = int(port_position.get('x')), int(port_position.get('y'))
        colors = self.colors.get('PortTypes').get(connection_to_draw.type)
        bg_color = tuple(colors.get('Background'))
        text_color = tuple(colors.get('Text'))

        self.sizes.connection_size = abs(self.sizes.connection_size)

        right_side = x > self.img.width/2

        draw = ImageDraw.Draw(self.img)
        height = self.sizes.name_height
        width = self.font.getlength(connection_to_draw.name)

        height /= 2

        if right_side:
            init_x = x + self.sizes.connection_size
            end_x = init_x + width

        else:
            init_x = x - self.sizes.connection_size - width
            end_x = init_x + width

        draw.rounded_rectangle(
            (
                init_x - self.sizes.name_border,
                y-height,
                end_x + self.sizes.name_border,
                y+height
            ),
            radius=self.sizes.name_border_radius,
            fill=bg_color
        )
        draw.text(
            (init_x, y),
            connection_to_draw.name,
            fill=text_color,
            font=self.font,
            anchor='lm'
        )

    def port(self, connection_to_draw: Connection):
        '''
        Desenha a conexão e o nome da conexão

        Parâmetros:
        ----------
        connection_to_draw: Connection
            Conexão a ser desenhada
        '''
        try:
            self.connection(connection_to_draw)
            self.name(connection_to_draw)
            self.board.connections.append(connection_to_draw.__dict__)
            self.board.used_types.append(connection_to_draw.type)
        except Exception as e:
            print('Erro ao desenhar a conexão: ', connection_to_draw.__dict__)
            print(e)

    def color_legend(self):
        '''
        Desenha uma paleta de cores no canto superior esquerdo
        '''

        colors = self.colors.get('PortTypes')

        x = 40
        y = 25

        draw = ImageDraw.Draw(self.img)
        multiplier = self.sizes.legend_multiplier

        for name, info in colors.items():
            if name not in self.board.used_types:
                continue

            bg_color = tuple(info.get('Background'))
            text_color = tuple(info.get('Text'))

            legend_font = self.font
            legend_font.size = legend_font.size*multiplier

            height = self.sizes.name_height*multiplier
            width = self.font.getlength(name)
            border = self.sizes.name_border*multiplier
            radius = self.sizes.name_border_radius*multiplier

            init_x = x
            end_x = init_x + width

            draw.rounded_rectangle(
                (
                    init_x - border,
                    y,
                    end_x + border,
                    y+height
                ),
                radius=radius,
                fill=bg_color
            )

            draw.text(
                (init_x+width/2, y+height/2),
                name,
                fill=text_color,
                font=legend_font,
                anchor='mm'
            )

            y += height + 10
