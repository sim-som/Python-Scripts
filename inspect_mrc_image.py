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
    angpix = float(f.voxel_size.x)


# %%
# img = filters.median(img)   # simple denoise
img = exposure.rescale_intensity(img) # rescaling float values so that min=-1.0 and max=+1.0


# %%
# crop the image to quadratic shape
shape_max = max(list(img.shape))
# %%
shape_min = min(list(img.shape))
diff = shape_max - shape_min

img_quad = img[:, diff//2 : shape_max - diff//2]


plt.figure(figsize=(12,6))
plt.subplot(121)
plt.imshow(filters.median(img), cmap="gray")

plt.subplot(122)
plt.imshow(filters.median(img_quad), cmap="gray")
plt.show()

# %%
# Calculate the power spectrum 
# (heavily inspired by https://bertvandenbroucke.netlify.app/2019/05/24/computing-a-power-spectrum-in-python/)

npix = img_quad.shape[0]

# complex fourier transform of the image:
fourier_image = fft.fftn(img_quad)
# absolute values of the complex amplidudes:
fourier_amplitudes = np.abs(fourier_image)**2
plt.imshow(np.log(fourier_amplitudes))

# %%
# spatial frequency / wave vector k

# get the corresponding values for the wave vector k
# multiplying by npix gives k in pixel frequency (unit: 1/px bzw. px^-1):
kfreq = fft.fftfreq(npix) * npix
# convert into 2D array:
kfreq2D = np.meshgrid(kfreq, kfreq)
# calculate the absolute value (or norm) for each (kx, ky) in kfreq2D:
knrm = knrm = np.sqrt(kfreq2D[0]**2 + kfreq2D[1]**2)

# %%
# binning

#flatten the 2 dim arrays to 1D:
knrm = knrm.flatten()
fourier_amplitudes = fourier_amplitudes.flatten()

# set up wave number bins to bin amplitudes in kspace
# kbins contains start and end points of all bins:
kbins = np.arange(0.5, npix//2 + 1, 1.)
# k values are the mid points of the bins:
kvals = 0.5 * (kbins[1:] + kbins[:-1])

# %%
# average radial amplitude (i.e. the power spectrum):

#calculate the average fourier amplitude for each bin:
from scipy import stats
Abins, _, _ = stats.binned_statistic(
    knrm, fourier_amplitudes,
    statistic="mean",
    bins=kbins
)
# multiply by volume of sperical shell defined by the bins (for 2D this is a surface area)
# Without multiplying the spectrum looks less "weird" and more similar to EMAN2 plot
# Abins *= np.pi * (kbins[1:]**2 - kbins[:-1]**2)/home/simon/gpu-rechner_u3_mount/cryoSPARC_projects/P20/J49/cryosparc_P20_J49_templates.mrc

#%%
kvals_ang = kvals / (npix * angpix)

def one_over(x):
    """Vectorized 1/x, treating x==0 manually"""
    x = np.array(x).astype(float)
    near_zero = np.isclose(x, 0)
    x[near_zero] = np.inf
    x[~near_zero] = 1 / x[~near_zero]
    return x

# corresponding lengthscale
xvals = one_over(kvals_ang)

# %%
# plot the powerspectrum
plt.figure(figsize=(12,6))
plt.plot(kvals_ang, Abins)
plt.xlabel("spatial frequency $k$ [1/Å]")
plt.ylabel("$P(k)$")
plt.title("Power spectrum")

# plt.xlim([kvals_ang.min(), kvals_ang.max()])

# setting up a secondary axis (see https://matplotlib.org/stable/gallery/subplots_axes_and_figures/secondary_axis.html):


ax = plt.gca()
secax = ax.secondary_xaxis("top", functions = (one_over, one_over))
secax.set_xlabel("length scale [Å]")

plt.show()

# %%
# plot the powerspectrum
plt.figure(figsize=(12,6))
plt.semilogy(kvals_ang, Abins)
plt.xlabel("spatial frequency $k$ [1/Å]")
plt.ylabel("$P(k)$")
plt.title("Power spectrum")

# plt.xlim([kvals_ang.min(), kvals_ang.max()])

# setting up a secondary axis (see https://matplotlib.org/stable/gallery/subplots_axes_and_figures/secondary_axis.html):


ax = plt.gca()
secax = ax.secondary_xaxis("top", functions = (one_over, one_over))
secax.set_xlabel("length scale [Å]")

plt.show()
# %%
# plot the powerspectrum
plt.figure(figsize=(12,6))
plt.loglog(kvals_ang, Abins)
plt.xlabel("spatial frequency $k$ [1/Å]")
plt.ylabel("$P(k)$")
plt.title("Power spectrum")

# plt.xlim([kvals_ang.min(), kvals_ang.max()])

# setting up a secondary axis (see https://matplotlib.org/stable/gallery/subplots_axes_and_figures/secondary_axis.html):


ax = plt.gca()
secax = ax.secondary_xaxis("top", functions = (one_over, one_over))
secax.set_xlabel("length scale [Å]")

plt.show()

# %%
