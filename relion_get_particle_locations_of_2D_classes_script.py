#%%
# imports
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from natsort import natsorted
import pandas as pd
from matplotlib import patches
import argparse
from progress.bar import Bar

from starparser import fileparser
import mrcfile
# %%
# file/directory management:
parser = argparse.ArgumentParser(description="""
    Get/Show the particles of a given class in the micrographs
""")
parser.add_argument("data_star_file_p", help="The path to the ..._data.star file")
parser.add_argument("class_id", help="ID of the class of interest (Get this from the relion gui)")
args = parser.parse_args()

data_star_file_p = Path(args.data_star_file_p)
# turn into absolute path if path is relative (likely):
data_star_file_p = data_star_file_p.resolve()

class_id = int(args.class_id)

print(data_star_file_p)

assert data_star_file_p.exists() and data_star_file_p.is_file()
job_dir_p = data_star_file_p.parent
assert len(job_dir_p.name) == 6 and job_dir_p.name[:3] == "job"
project_dir_p = job_dir_p.parents[1]
assert project_dir_p.exists() and project_dir_p.is_dir()
img_stack_file_p = job_dir_p / Path(data_star_file_p.name[:-10] + "_classes.mrcs")
assert img_stack_file_p.exists() and img_stack_file_p.is_file()

#%%
# parse the _data.star file
particles, metadata = fileparser.getparticles(str(data_star_file_p))
# convert numerical columns to float or int:
particles = particles.apply(pd.to_numeric, errors="ignore")
# %% 
# load img stack containing 2D classes
with mrcfile.open(img_stack_file_p) as f:
    stack = f.data
    print(stack.shape)

# %%
# pixel size:data_star_file_p
data_star_file_p
with mrcfile.open(img_stack_file_p) as f:
    angpix = f.voxel_size.x
    print("pixel size (Å):", angpix)
TMV_width = 180 / angpix

# %%
# # show all classes

# def plot_all(images):
#     N = images.shape[0]
#     rc = np.sqrt(N)
#     rc = int(np.ceil(rc))
#     print(rc)
#     fig, axs = plt.subplots(rc, rc, figsize=(12,12))
#     axs = axs.flatten()
#     # remove ticks:
#     for i in range(len(axs)):
#         axs[i].set_xticks([])
#         axs[i].set_yticks([])
#     # plot images:
#     for i in range(N):
#         axs[i].imshow(images[i, :, :])
#         axs[i].set_xlabel(f"Class {i+1}")
#     fig.suptitle("2D classes")
#     plt.tight_layout()
    
# plot_all(stack)
# %%


class_particles = particles[particles["_rlnClassNumber"] == class_id]
N_part = len(class_particles)

# %%
# Show selected class:
plt.figure("2D Class")
plt.imshow(stack[class_id - 1, :, :])   # watch out class IDs start at 1!
plt.title(f"Class {class_id} of {job_dir_p}")
plt.xlabel(f"Nr. particles {N_part}")
plt.show()

# %%
# plot micrographs together with particles of selected class:
def draw_particle(x, y, radius):
    
    circle = patches.Circle(
        (x, y),
        radius=radius,
        color="tab:green",
        fill = False
    )
    ax.add_patch(circle)

plt.ioff()

micrographs = pd.unique(class_particles["_rlnMicrographName"])
with Bar("Loading Images ...", max = len(micrographs)) as b:
    for mic in micrographs:
        # correct full path of micrograph:
        mic_p = project_dir_p / Path(mic)
        assert mic_p.exists() and mic_p.is_file()
        # data for just the micrograph:
        image_class_particles = class_particles[class_particles["_rlnMicrographName"] == mic]
        # load the micrograph and plot:
        fig, ax = plt.subplots()
        plt.gray()
        with mrcfile.open(mic_p) as f:
            plt.imshow(f.data)
        # draw coordinates on image:
        for x, y in zip(image_class_particles["_rlnCoordinateX"], image_class_particles["_rlnCoordinateY"]):
            draw_particle(x, y, TMV_width/2.)
        ax.set_title(f"Coords. $\in$ Class {class_id} of {job_dir_p}")
        ax.set_xlabel(mic_p.name)
        b.next()


# for i in plt.get_fignums():
#     plt.figure(i)
#     figMng = plt.get_current_fig_manager()
#     figMng.window.showMaximized()
#     plt.show()

# figMng = plt.get_current_fig_manager()
# figMng.window.showMaximized()
plt.show()

