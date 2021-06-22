import sys

import numpy as np
import matplotlib.pyplot as plt
import urllib.request

from PIL import Image

from src import config, functions

image_to_read = Image.open(sys.argv[1])

# Transformo la imagen en un array de NumPy.
image = np.array(image_to_read)

print(f'Dimensiones de la imagen: {image.shape}')  # filas, columnas y capas.
