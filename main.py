import sys

import numpy as np
import matplotlib.pyplot as plt
import urllib.request

from PIL import Image

from src import config, functions


byte_list = functions.get_bytes(sys.argv[1])

print(f'{sys.argv[1]}: {byte_list}')

msg_len_bin = bin(len(byte_list))[2:].zfill(config.OP_GET_MSG_BYTES)
print(f'Msg lenght: {msg_len_bin} ({len(byte_list)})')

url = 'https://www.beatchapter.com/ekmps/shops/beatchapter/images/time-out-magazine-december-17-23-1971-frank-zappa-4-page-interview-a-4-page-island-records-advert-16746-p.jpg'  # noqa: E501
image_from_internet = Image.open(urllib.request.urlopen(url))

# Transformo la imagen en un array de NumPy.
image = np.array(image_from_internet)

plt.figure(figsize=(10, 20))
plt.imshow(image)
plt.show()

# Veo la forma.
print(image.shape)  # filas, columnas y profundidad (capas RGB)

total_pixels = np.prod(image.shape)  # x*y*z
print(f'Total pixels: {total_pixels}')

# Ahora veo cómo obtener el valor de un pixel, por ejemplo el primero: 0x0
print(f'Los 3 colores del pixel son: {image[0, 0]}')

pixels = int(np.ceil(config.OP_GET_MSG_BYTES/3))

print(f'Voy a usar {pixels} píxeles para almacenar OP_GET_MSG_BYTES.')

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
