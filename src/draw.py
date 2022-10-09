from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype('./data/Roboto-Black.ttf')


class Colors:
    CONNECTION = (188, 198, 198, 255)

    PORT_TYPES = {
        'Default': {
            'bg': (241, 196, 55, 255),
            'text': (255, 255, 255, 255)
        },
        'Ground': {
            'bg': (23, 30, 33, 255),
            'text': (255, 255, 255, 255)
        },
        'Power': {
            'bg': (192, 34, 21, 255),
            'text': (255, 255, 255, 255)
        }
    }


class Sizes:
    CONNECTION_RADIUS = 6
    CONNECTION_SIZE = 100
    CONNECTION_WIDTH = 2

    NAME_BORDER_RADIUS = 10
    NAME_HEIGHT = 30
    LOWER_NAME_WIDTH = 9.5
    UPPER_NAME_WIDTH = 13.5
    NAME_BORDER = 10


def get_name_width(name: str) -> int:
    '''
    Retorna a largura do nome da conexão

    Parâmetros:
    ----------
    name: str
        Nome da conexão

    Retorno:
    -------
    width: int
        Largura do nome da conexão
    '''
    upper = sum(1 for c in name if c.isupper())
    lower = sum(1 for c in name if c.islower())
    numbers = sum(1 for c in name if c.isdigit())
    others = sum(1 for c in name if not c.isalnum())

    width = Sizes.UPPER_NAME_WIDTH * upper
    width += Sizes.LOWER_NAME_WIDTH * lower
    width += Sizes.LOWER_NAME_WIDTH * numbers
    width += Sizes.LOWER_NAME_WIDTH * others*0.6

    return width


def input_arrow(img: Image, port: str, ports_info: dict):
    '''
    Desenha a seta de entrada

    Parâmetros:
    ----------
    img: Image
        Imagem a ser desenhada

    port: str
        Pino a ser desenhado

    ports_info: dict
        Dicionário com as informações dos pinos

    Retorno:
    -------
    ImageDraw
        Imagem com a seta de entrada desenhada
    '''
    port_position = ports_info.get('Ports').get(port)

    x, y = int(port_position.get('x')), int(port_position.get('y'))

    draw = ImageDraw.Draw(img)

    draw.line(
        (
            int(x-(Sizes.CONNECTION_SIZE*0.6)),
            y,
            int(x-(Sizes.CONNECTION_SIZE*0.6)-10),
            y-10
        ),
        fill=Colors.CONNECTION,
        width=Sizes.CONNECTION_WIDTH,
        joint='curve'
    )

    draw.line(
        (
            int(x-(Sizes.CONNECTION_SIZE*0.6)),
            y,
            int(x-(Sizes.CONNECTION_SIZE*0.6)-10),
            y+10
        ),
        fill=Colors.CONNECTION,
        width=Sizes.CONNECTION_WIDTH,
        joint='curve'
        )


def output_arrow(img: Image, port: str, ports_info: dict):
    '''
    Desenha a seta de saída

    Parâmetros:
    ----------
    img: Image
        Imagem a ser desenhada

    port: str
        Pino a ser desenhado

    ports_info: dict
        Dicionário com as informações dos pinos

    Retorno:
    -------
    ImageDraw
        Imagem com a seta de saída desenhada
    '''
    port_position = ports_info.get('Ports').get(port)

    x, y = int(port_position.get('x')), int(port_position.get('y'))

    draw = ImageDraw.Draw(img)

    draw.line(
        (
            int(x-(Sizes.CONNECTION_SIZE*0.7)),
            y,
            int(x-(Sizes.CONNECTION_SIZE*0.7)+10),
            y-10
        ),
        fill=Colors.CONNECTION,
        width=Sizes.CONNECTION_WIDTH,
        joint='curve'
    )

    draw.line(
        (
            int(x-(Sizes.CONNECTION_SIZE*0.7)),
            y,
            int(x-(Sizes.CONNECTION_SIZE*0.7)+10),
            y+10
        ),
        fill=Colors.CONNECTION,
        width=Sizes.CONNECTION_WIDTH,
        joint='curve'
    )


def connection(img: Image, port: str, in_out: str, ports_info: dict):
    '''
    Desenha uma conexão em um pino específico

    Parâmetros:
    ----------
    img: Image
        Imagem a ser desenhada

    port: str
        Pino a ser desenhado

    ports_info: dict
        Dicionário com as informações dos pinos

    Retorno:
    -------
    ImageDraw
        Imagem com a conexão desenhada
    '''
    connection_radius = int(ports_info.get('PortSize'))/Sizes.CONNECTION_RADIUS

    port_position = ports_info.get('Ports').get(port)

    x, y = int(port_position.get('x')), int(port_position.get('y'))

    draw = ImageDraw.Draw(img)
    draw.ellipse(
        (
            x-connection_radius,
            y-connection_radius,
            x+connection_radius,
            y+connection_radius
        ),
        fill=Colors.CONNECTION
    )

    draw.line(
        (x, y, x-Sizes.CONNECTION_SIZE, y),
        fill=Colors.CONNECTION,
        width=Sizes.CONNECTION_WIDTH,
        joint='curve'
    )

    if in_out == 'in':
        input_arrow(img, port, ports_info)

    if in_out == 'out':
        output_arrow(img, port, ports_info)


def name(img: Image, port: str, name: str, port_type: str, ports_info: dict):
    '''
    Desenha o nome da conexão

    Parâmetros:
    ----------
    img: Image
        Imagem a ser desenhada

    port: str
        Pino a ser desenhado

    name: str
        Nome da conexão

    port_type: str
        Tipo da conexão

    ports_info: dict
        Dicionário com as informações dos pinos

    Retorno:
    -------
    ImageDraw
        Imagem com o nome da conexão desenhado
    '''
    port_position = ports_info.get('Ports').get(port)

    x, y = int(port_position.get('x')), int(port_position.get('y'))

    draw = ImageDraw.Draw(img)
    height = Sizes.NAME_HEIGHT

    width = get_name_width(name)

    height /= 2
    width /= 2

    end_x = x - Sizes.CONNECTION_SIZE
    init_x = end_x - width

    bg_color = Colors.PORT_TYPES.get(port_type).get('bg')
    text_color = Colors.PORT_TYPES.get(port_type).get('text')

    draw.rounded_rectangle(
        (
            init_x - Sizes.NAME_BORDER/2,
            y-height,
            end_x + Sizes.NAME_BORDER/2,
            y+height
        ),
        radius=Sizes.NAME_BORDER_RADIUS,
        fill=bg_color
    )

    draw.text(
        (init_x, y),
        name,
        fill=text_color,
        font=font,
        anchor='lm'
    )


def all_port(img: Image, port: str, port_name: str, in_out: str, port_type: str, ports_info: dict):
    '''
    Desenha todos os elementos de uma conexão

    Parâmetros:
    ----------
    img: Image
        Imagem a ser desenhada

    port: str
        Pino a ser desenhado

    port_name: str
        Nome da conexão

    port_type: str
        Tipo da conexão

    ports_info: dict
        Dicionário com as informações dos pinos

    Retorno:
    -------
    ImageDraw
        Imagem com todos os elementos da conexão desenhados
    '''
    connection(img, port, in_out, ports_info)
    name(img, port, port_name, port_type, ports_info)
