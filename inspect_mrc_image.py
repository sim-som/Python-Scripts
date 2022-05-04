#%%
# imports
import mrcfile
import numpy as np
from numpy import fft
from matplotlib import pyplot as plt
from pathlib import Path
from skimage import io, util, exposure, filters
# %%
mrc_file_p = Path(
    "/home/simon/gpu-rechner_u3_mount/cryoSPARC_projects/P20/J88/motioncorrected/013361838351298364391_FoilHole_15362370_Data_15372558_15372560_20211015_235110_fractions.mrc_patch_aligned_doseweighted.mrc"
)
assert mrc_file_p.exists() and mrc_file_p.is_file()

# %%
# read the image data into numpy array and the pixel size
with mrcfile.open(mrc_file_p) as f:
    img:np.ndarray = f.data
    angpix = f.voxel_size.x
    
# %%
img = filters.median(img)   # simple denoise
img = exposure.rescale_intensity(img) # rescaling float values so that min=-1.0 and max=+1.0
# %%
plt.imshow(img, cmap="gray")

# %%
# crop the image to quadratic shape
shape_max = max(list(img.shape))
shape_min = min(list(img.shape))
diff = shape_max - shape_min

img_quad = img[:, diff//2 : shape_max - diff//2]

plt.imshow(img_quad, cmap="gray")


# %%
# Calculate the power spectrum

# take the fourier transform of the image
F = fft.fft2(img_quad)
# shift the quadrants around so that low
# spatial freqs. are in the center of the 2D fourier transformed image
F = fft.fftshift(F)
ps_2d = np.abs(F)**2

#%%
plt.imshow(np.log(ps_2d), cmap="gray")
# %%
# calculate the radial profile:

def radial_profile(data, center = None):

    if center == None:
        center = np.array(data.shape) // 2
    
    y, x = np.indices(data.shape)

    y_center, x_center = center

    # calculate radial distances:
    r = np.sqrt( (x-x_center)**2 + (y - y_center)**2)
    r = r.astype(int)
    
    tbin = np.bincount(r.ravel(), data.ravel())
    nr = np.bincount(r.ravel())
    radialprofile = tbin / nr
    return radialprofile

ps_1d = radial_profile(ps_2d)
# %%
plt.loglog(ps_1d)

# %%
