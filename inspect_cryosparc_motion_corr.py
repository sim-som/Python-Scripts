#%%
# imports
import numpy as np
import pandas as pd
import pyem
import matplotlib.pyplot as plt
from pathlib import Path
import mrcfile
 # %%
# .npy files:
motion_corr_dir_p = Path(
    "/home/simon/gpu-rechner_u3_mount/cryoSPARC_projects/P20/J5/motioncorrected"
)
# %%
# print out file content:
for file in motion_corr_dir_p.glob("*.npy"):
    print(file.name)
    cs = np.load(file)
    print(cs.shape)
    print(cs)

# %%
# rigid trajectories:
rigid_motion_tab = {
    "micrograph": [],
    "x_trajectory": [],
    "y_trajectory": []
}

for file in motion_corr_dir_p.glob("*rigid*.npy"):
    #save into dict:

    cs = np.load(file)
    # discard redundant dimension:
    cs = cs[0]

    rigid_motion_tab["micrograph"].append(file.name)
    rigid_motion_tab["x_trajectory"].append(cs[:,0])
    rigid_motion_tab["y_trajectory"].append(cs[:,1])

rigid_motion_tab["x_trajectory"] = np.array(rigid_motion_tab["x_trajectory"])
rigid_motion_tab["y_trajectory"] = np.array(rigid_motion_tab["y_trajectory"])

# %%
# rigid trajectories:
rigid_motion = {}
bending_motion = {}

for traj_file in motion_corr_dir_p.glob("*rigid*.npy"):

    print(traj_file.name)

    raw_data = np.load(traj_file)
    # discard redundant dimension:
    raw_data = raw_data[0]

    # save into dict:
    rigid_motion[traj_file.name] = raw_data


# %%

for traj_file, traj in rigid_motion.items():

    #plot trajectories:
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
    corr_img_file_p = motion_corr_dir_p / Path(traj_file.split(".")[0] + ".mrc_patch_aligned_doseweighted.mrc")
    assert corr_img_file_p.exists() and corr_img_file_p.is_file()

    with mrcfile.open(corr_img_file_p) as f:
        plt.figure()
        plt.gray()
        plt.imshow(f.data)
        plt.title(f"Corrected image {corr_img_file_p.name}")
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

for traj_file in motion_corr_dir_p.glob("*bending_traj.npy"):

    print(traj_file.name)

    raw_data = np.load(traj_file)
    print(raw_data)
    
    # save into dict:
    # rigid_motion[traj_file.name] = raw_data

    break

# %%
