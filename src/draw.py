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

    def input_arrow(self, x, y, connection_color, draw):
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

    def output_arrow(self, x, y, connection_color, draw):
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
        connection_color = tuple(self.board.colors.get('Connection'))

        right_side = x > self.img.width/2

        if right_side:
            self.sizes.connection_size = -abs(self.sizes.connection_size)

            if connection_to_draw.in_out == 'in':
                connection_to_draw.in_out = 'out'
            elif connection_to_draw.in_out == 'out':
                connection_to_draw.in_out = 'in'

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

        if connection_to_draw.in_out == 'in':
            self.input_arrow(x, y, connection_color, draw)

        elif connection_to_draw.in_out == 'out':
            self.output_arrow(x, y, connection_color, draw)

        elif connection_to_draw.in_out == 'in_out':
            self.output_arrow(x-15, y, connection_color, draw)
            self.input_arrow(x+15, y, connection_color, draw)

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
        except Exception as e:
            print('Erro ao desenhar a conexão: ', connection_to_draw.__dict__)
            print(e)
