import sys

import numpy as np
import matplotlib.pyplot as plt
import urllib.request

from PIL import Image

from src import config, functions


byte_list = functions.get_bytes(sys.argv[1])

print(f'{sys.argv[1]}: {byte_list}')

msg_len_bin = bin(len(byte_list))[2:].zfill(config.OP_GET_MSG_BYTES)
print(f'Msg lenght: {msg_len_bin} ({len(byte_list)} Bytes)')

pixels = int(np.ceil(config.OP_GET_MSG_BYTES/3))

print(f'Voy a usar {pixels} píxeles ({pixels*3} bits) para almacenar OP_GET_MSG_BYTES.')  # noqa: E501
print(f'Voy a usar {len(byte_list)*config.BITS_X_CHAR} bits para el mensaje.')

url = 'https://www.beatchapter.com/ekmps/shops/beatchapter/images/time-out-magazine-december-17-23-1971-frank-zappa-4-page-interview-a-4-page-island-records-advert-16746-p.jpg'  # noqa: E501
image_from_internet = Image.open(urllib.request.urlopen(url))

# Transformo la imagen en un array de NumPy.
image = np.array(image_from_internet)

plt.figure(figsize=(10, 20))
plt.imshow(image)
plt.show()

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

# Creo filtro para saber qué pixel tiene que ser impar (0) y cuál par (1).
h_filter = np.array(
    [list(msg_len_bin[i:i+3]) for i in range(0, len(msg_len_bin), 3)],
    dtype=int
)

# Imprimo el filtro para ver cómo queda.
print('h_filter:')
print(h_filter)

header = image[0, :pixels]
# Imprimo los 4 primeros píxeles a los que voy a aplicar el filtro.
print('header:')
print(header)

header[header % 2 == h_filter] -= 1

print('header tras pasarle el filtro:')
print(header)
