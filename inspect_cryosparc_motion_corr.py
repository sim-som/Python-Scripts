#%%
# imports
import numpy as np
import random
from skimage import io
import matplotlib.pyplot as plt
from pathlib import Path
import mrcfile
 # %%
# .npy files:
dir_p = Path(
    "/home/simon/gpu-rechner_u3_mount/cryoSPARC_projects/P20/J5/motioncorrected"
)
thumbnails_dir_p = Path(
    "/home/simon/gpu-rechner_u3_mount/cryoSPARC_projects/P20/J5/thumbnails"
)
# %%
# print out file content:
for file in dir_p.glob("*.npy"):
    print(file.name)
    cs = np.load(file)
    print(cs.shape)
    print(cs)

    break

# %%
# rigid trajectories:
rigid_motion = {}
bending_motion = {}

for traj_file in dir_p.glob("*rigid*.npy"):

    print(traj_file.name)

    raw_data = np.load(traj_file)
    # discard redundant dimension:
    raw_data = raw_data[0]

    # save into dict:
    rigid_motion[traj_file.name] = raw_data


# %%
# Sample random subset and plot trajectories:
N_sample = 10
samples = dict(random.sample(list(rigid_motion.items()), N_sample))

def get_thumbnail_path(img_key:str) -> Path:
    ## get image filename from trajectory filename:
    thumb_corr_img_p = thumbnails_dir_p / Path(img_key.split(".")[0] + ".mrc_thumb_@2x.png")
    assert thumb_corr_img_p.exists() and thumb_corr_img_p.is_file()
    return thumb_corr_img_p


for traj_file, traj in samples.items():

    plt.figure(figsize=(18,6))


    plt.subplot(131)
    plt.plot(traj[:,0], traj[:,1])
    plt.xlabel("x (?)")
    plt.ylabel("y (?)")

    plt.subplot(132)
    plt.plot(traj[:,0])
    plt.title("x-motion (?)")

    plt.subplot(133)
    plt.plot(traj[:,1])
    plt.title("y-motion (?)")

    plt.suptitle(traj_file)

    plt.show()

    # plot image:
    ## get image filename from trajectory filename:
    thumb_corr_img_p = get_thumbnail_path(traj_file)
    img = io.imread(thumb_corr_img_p)
    
    plt.figure()
    plt.gray()
    plt.imshow(img)
    plt.title(f"Corrected image {thumb_corr_img_p.name}")
    plt.show()

    # break    


# %%
# Calculate Sum of traveled path:

def one_dim_stepwise_dist(a:np.array):
    a_iplus1 = np.roll(a, -1)[:-1]
    step_dist = a_iplus1 - a[:-1]
    assert len(a) == len(step_dist) + 1
    return step_dist

def sum_of_traveled_dist(x_traj:np.array, y_traj:np.array):
    assert len(x_traj) == len(y_traj)
    # traveled distance:
    dist_x = one_dim_stepwise_dist(x_traj)
    dist_y = one_dim_stepwise_dist(y_traj)

    squared_distances = dist_x**2 + dist_y**2
    dist = np.sqrt(squared_distances)
    
    return dist.sum()

test_x, test_y = list(rigid_motion.values())[0][:,0], list(rigid_motion.values())[0][:,1]
sum_dist = sum_of_traveled_dist(test_x, test_y)
        
# %%
# for all images:
sum_dist = []
for traj_file, traj in rigid_motion.items():

    sum_dist.append(sum_of_traveled_dist(traj[:,0], traj[:,1]))


# %%
# plot sum dist for each image:
plt.figure(figsize=(12,6))

plt.subplot(121)
plt.plot(sum_dist)
plt.xlabel("Image ID")
plt.ylabel("overall drift")

plt.subplot(122)
plt.hist(sum_dist, bins="auto")
plt.xlabel("overall drift")
plt.ylabel("counts")

plt.suptitle("Total rigid drift during Acquisition as estimated by cryoSPARC")

plt.show()
# %%
# bending trajectories:
bending_motion = {}

for traj_file in dir_p.glob("*bending_traj.npy"):

    # print(traj_file.name)

    raw_data = np.load(traj_file)

    # x-component and y components of vector field:
    U = raw_data[0, 1, :, :]
    V = raw_data[1, 1, :, :]

    # print("x component:")
    # print(X)
    # print("y component:")
    # print(Y)
    
    # save into dict:
    bending_motion[traj_file.name] = (U, V)

# %%
# Sample random subset and plot:
N_sample = 10
samples = dict(random.sample(list(bending_motion.items()), N_sample))
XXXoutfileXXX
for key, val in samples.items():

    # vector components:
    U = val[0]
    V = val[1]

    thumb = io.imread(get_thumbnail_path(key))

    # coordinates in the thumbnail:
    y = np.linspace(0, thumb.shape[0], U.shape[0])
    x = np.linspace(0, thumb.shape[1], U.shape[1])

    X, Y = np.meshgrid(x, y, indexing="ij")
    
    plt.figure(figsize=(12,18))
    plt.subplot(211)
    plt.imshow(thumb)
    plt.title("Image thumbnail")
    # plt.quiver(X, Y, U, V)

    plt.subplot(212)
    plt.quiver(U, V, color = "tab:red")
    plt.title("Bending patch motion")

    plt.suptitle(key)
    plt.show()

# %%
example_img_file = "FoilHole_15359488_Data_15372558_15372560_20211015_181243_fractions.mrc"
for key, val in bending_motion.items():
    if example_img_file in key:
        # get vector components
        U = val[0]
        V = val[1]
        # read motion corrected image:
        with mrcfile.open(dir_p / Path(example_img_file)) as f:
            img = f.data
        
        plt.figure()
        plt.imshow(img)
        plt.quiver(U, V)
        plt.title(key)
        plt.show()
# %%
