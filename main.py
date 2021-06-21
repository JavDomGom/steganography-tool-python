import sys

import numpy as np
import matplotlib.pyplot as plt
import urllib.request

from PIL import Image

from src import config, functions


byte_list = functions.get_bytes(sys.argv[1])
len_msg = len(byte_list)
print(f'{sys.argv[1]}: {byte_list}')

msg_len_bin = bin(len_msg)[2:].zfill(config.OP_GET_MSG_BYTES)
print(f'Msg lenght: {msg_len_bin} ({len_msg} Bytes)')

pixels = int(np.ceil(config.OP_GET_MSG_BYTES/3))

print(f'Voy a usar {pixels} píxeles ({pixels*3} bits) para almacenar OP_GET_MSG_BYTES.')  # noqa: E501
print(f'Voy a usar {len_msg*config.BITS_X_CHAR} bits para el mensaje.')

# url = 'https://www.beatchapter.com/ekmps/shops/beatchapter/images/time-out-magazine-december-17-23-1971-frank-zappa-4-page-interview-a-4-page-island-records-advert-16746-p.jpg'  # noqa: E501
url = 'https://d25rq8gxcq0p71.cloudfront.net/dictionary-images/324/f2101e8b-0ae8-4a78-b1f5-4242b6dba0c4.jpg'  # noqa: E501
image_from_internet = Image.open(urllib.request.urlopen(url))

# Transformo la imagen en un array de NumPy.
image = np.array(image_from_internet)

height, width, depth = image.shape
dpi = 80
figsize = width / float(dpi), height / float(dpi)

fig = plt.figure(figsize=figsize)
# plt.imshow(image)
fig.figimage(image)
# plt.show()

# Veo la forma.
print(f'Dimensiones de la imagen: {image.shape}')  # filas, columnas y capas.

total_pixels = np.prod(image.shape)  # filas x columnas x capas
bits_available_to_msg = total_pixels*3-config.OP_GET_MSG_BYTES
print(f'Bits reservados para la cabecera: {config.OP_GET_MSG_BYTES}')
print(f'Bits disponibles para el mensaje: {bits_available_to_msg}')
print(f'Total bits: {total_pixels*3}')
print(f'Total pixels: {total_pixels}')
print(f'Longitud máxima del mensaje en imagen: {bits_available_to_msg/8}')

# Ahora veo cómo obtener el valor de un pixel, por ejemplo el primero: 0x0
print(f'Los 3 colores del pixel son: {image[0, 0]}')

h_filter = functions.get_filter(msg_len_bin)

# Imprimo el filtro para ver cómo queda.
print('h_filter:')
print(h_filter)

header = image[0, :pixels]

# Imprimo los 4 primeros píxeles a los que voy a aplicar el filtro.
print('header:')
print(header)

functions.apply_filter(header, h_filter)

print('header tras pasarle el filtro:')
print(header)

pixels_to_msg = int(np.ceil(len_msg*config.BITS_X_CHAR/3))
print(f'Voy a usar {pixels_to_msg} pixeles para el mensaje.')

bits_string = ''.join(byte_list).ljust(pixels_to_msg*3, '0')
print(f'bits_string: {bits_string}')

b_filter = functions.get_filter(bits_string)

print('b_filter:')
print(b_filter)

# -----------------------------------------------------------------------------

body = image[0, pixels:pixels+pixels_to_msg]
print('body:')
print(body)

functions.apply_filter(body, b_filter)

print('body tras pasarle el filtro:')
print(body)

# -----------------------------------------------------------------------------

total_pixels_used = image[0, :pixels+pixels_to_msg]
print('total_pixels_used:')
print(total_pixels_used)

plt.axis('off')
fig.savefig(url.split('/')[-1], bbox_inches='tight', pad_inches=0)
# plt.show()
