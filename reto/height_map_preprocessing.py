# ------------------------------------------------------------------------------------------------------------------
#   Height map pre-processing
# ------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------
#   Imports
# ------------------------------------------------------------------------------------------------------------------
import copy
import numpy as np
from skimage.transform import downscale_local_mean

import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

import plotly.graph_objects as px

# ------------------------------------------------------------------------------------------------------------------
#   File names
# ------------------------------------------------------------------------------------------------------------------
input_file = "mars_map.img"
output_file = "mars_map.npy"

# ------------------------------------------------------------------------------------------------------------------
#   Load map data
# ------------------------------------------------------------------------------------------------------------------

data_file = open(input_file, "rb")

endHeader = False
while not endHeader:
    line = data_file.readline().rstrip().lower()

    sep_line = line.split(b'=')

    if len(sep_line) == 2:
        itemName = sep_line[0].rstrip().lstrip()
        itemValue = sep_line[1].rstrip().lstrip()

        if itemName == b'valid_maximum':
            maxV = float(itemValue)
        elif itemName == b'valid_minimum':
            minV = float(itemValue)
        elif itemName == b'lines':
            n_rows = int(itemValue)
        elif itemName == b'line_samples':
            n_columns = int(itemValue)
        elif itemName == b'map_scale':
            scale_str = itemValue.split()
            if len(scale_str) > 1:
                scale = float(scale_str[0])

    elif line == b'end':
        endHeader = True
        char = 0
        while char == 0 or char == 32:
            char = data_file.read(1)[0]
        pos = data_file.seek(-1, 1)

image_size = n_rows * n_columns
data = data_file.read(4*image_size)

image_data = np.frombuffer(data, dtype=np.dtype('f'))
image_data = image_data.reshape((n_rows, n_columns))
image_data = np.array(image_data)
image_data = image_data.astype('float64')

image_data = image_data - minV
image_data[image_data < -10000] = -1

# ------------------------------------------------------------------------------------------------------------------
#   Subsampling
# ------------------------------------------------------------------------------------------------------------------
sub_rate = round(10/scale)

image_data = downscale_local_mean(image_data, (sub_rate, sub_rate))
image_data[image_data < 0] = -1

print('Sub-sampling:', sub_rate)

new_scale = scale*sub_rate
print('New scale:', new_scale, 'meters/pixel')

# ------------------------------------------------------------------------------------------------------------------
#   Save map
# ------------------------------------------------------------------------------------------------------------------
np.save(output_file, image_data)

# ------------------------------------------------------------------------------------------------------------------
#   Show 3D surface
# ------------------------------------------------------------------------------------------------------------------

x = new_scale*np.arange(image_data.shape[1])
y = new_scale*np.arange(image_data.shape[0])
X, Y = np.meshgrid(x, y)

fig = px.Figure(data=px.Surface(x=X, y=Y, z=np.flipud(image_data), colorscale='hot', cmin=0,
                                lighting=dict(
                                    ambient=0.0, diffuse=0.8, fresnel=0.02, roughness=0.4, specular=0.2),
                                lightposition=dict(x=0, y=n_rows/2, z=2*maxV)),

                layout=px.Layout(scene_aspectmode='manual',
                                 scene_aspectratio=dict(
                                     x=1, y=n_rows/n_columns, z=max((maxV-minV)/x.max(), 0.2)),
                                 scene_zaxis_range=[0, maxV-minV])
                )

fig.show()

# ------------------------------------------------------------------------------------------------------------------
#   Show surface image
# ------------------------------------------------------------------------------------------------------------------

cmap = copy.copy(plt.cm.get_cmap('autumn'))
cmap.set_under(color='black')

ls = LightSource(315, 45)
rgb = ls.shade(image_data, cmap=cmap, vmin=0,
               vmax=image_data.max(), vert_exag=2, blend_mode='hsv')

fig, ax = plt.subplots()

im = ax.imshow(rgb, cmap=cmap, vmin=0, vmax=image_data.max(),
               extent=[0, scale*n_columns, 0, scale*n_rows],
               interpolation='nearest', origin='upper')

cbar = fig.colorbar(im, ax=ax)
cbar.ax.set_ylabel('Altura (m)')

plt.title('Superficie de Marte')
plt.xlabel('x (m)')
plt.ylabel('y (m)')

plt.show()

# ------------------------------------------------------------------------------------------------------------------
#   End of file
# ------------------------------------------------------------------------------------------------------------------
