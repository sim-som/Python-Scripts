# %%
import random
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import pandas as pd
from pandas import DataFrame
import mrcfile
from matplotlib.patches import Rectangle
from skimage.filters import median
from skimage.exposure import equalize_hist
# own module:
sys.path.insert(0, "/home/simon/code/cryolo_cbox_utils")
import cryolo_cbox_utils as cbox
# %%
# Functions:

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.
    Credit: https://stackoverflow.com/questions/14720331/how-to-generate-random-colors-in-matplotlib#25628397'''
    return plt.cm.get_cmap(name, n)


def add_particle_rectangle(axes, x_coord, y_coord, height, width, color, angle=0):

    # anchor_point_xy = (x_coord - width/2, y_coord-height/2)
    anchor_point_xy = (x_coord, y_coord)

    rect = Rectangle(
        xy=anchor_point_xy,
        width=width,
        height=height,
        color=color,
        angle=angle,
        fill=False,
        alpha=0.1
    )

    axes.add_patch(rect)


def plot_image_and_particles(img, particles_df:DataFrame, confidence_ths = 0.3):

    assert confidence_ths <=1 and confidence_ths > 0 
    
    plt.imshow(img, cmap="gray")

    ax = plt.gca()
    
    num_filaments = particles_df.filamentid.max()
    cmap_generator = get_cmap(num_filaments)


    for filament_id, filament_particles_df in particles_df.groupby("filamentid"):
        filament_id = int(filament_id)
    
        for i, part in filament_particles_df.iterrows():
            
            add_particle_rectangle(ax,
                x_coord=part.CoordinateX,
                y_coord=part.CoordinateY,
                width=part.Width,
                height=part.Height,
                color=cmap_generator(filament_id),
                angle=part.Angle
            )
    
    plt.xlabel(f"Confidence >= {confidence_ths}")

def get_warp_defocus(img_file):

    log_file_suffix = "_ctffind3.log"

    ctf_logfile = Path(img_file.parent / Path(f"{img_file.stem}{log_file_suffix}"))
    assert ctf_logfile.exists() and ctf_logfile.is_file()
    
    logfile_rows = []
    with open(ctf_logfile, mode="r") as f:
        for row in f:
            logfile_rows.append(row)
    last_row = logfile_rows[-1].split()
    defocus_x, defocus_y = last_row[:2]
    
    return defocus_x, defocus_y




# %%
images_dir = Path("/home/simon/simon_data/image_data/cryoem_data/arctica/20221129_SiSo_Ins_Fib_Fractions/average")
img_file_regex = "*.mrc"
boxed_particles_dir = Path("/home/simon/simon_data/image_data/cryoem_data/arctica/20221129_SiSo_Ins_Fib_Fractions/cryolo_automated_picking_output_boxes/CBOX_FILAMENT_SEGMENTED")
N = 10 # number of image particle pairs

# %%
all_img_files = list(images_dir.glob(img_file_regex))

# %%
defocii_x = []
defocii_y = []
for imfile in all_img_files:
    d = get_warp_defocus(imfile)
    defocii_x.append(d[0])
    defocii_y.append(d[1])
defocii_x = np.array(defocii_x, dtype=float)
defocii_y = np.array(defocii_y, dtype=float)
#%%
plt.figure()
plt.plot(defocii_x, ".", label="Defocus x", alpha=0.5)
plt.plot(defocii_y, ".", label="Defocus y", alpha=0.3)
plt.legend()
plt.show()

plt.figure()
plt.hist(defocii_x, bins="auto")
plt.hist(defocii_y, bins="auto", alpha = 0.3)
plt.show()

# %%
sampled_img_files = random.sample(all_img_files, 1)

# %%
for imfile in sampled_img_files:
    print("Image file:", imfile.name)

    cbox_file = boxed_particles_dir / f"{imfile.stem}.cbox"
    print("cbox file:", cbox_file)

    if not cbox_file.exists():
        print("No picked particles for this image")
        continue

    # parse .cbox file content:
    particles_df = cbox.parse_new_cbox_format(cbox_file)

    with mrcfile.open(imfile) as mrc:
        img = mrc.data
    img = median(img)
    # img = equalize_hist(img)

    plt.figure(imfile.name, figsize=(12,12))

    plot_image_and_particles(img, particles_df)

    plt.title(imfile.name)
    plt.show()

    

# %%