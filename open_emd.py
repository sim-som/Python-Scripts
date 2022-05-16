#%%
from hyperspy import api as hs
from skimage import io

# %%
# Load the image:
example_emd_file = "5I-No_Treh-TMV_1to100_in_H2O 20220208 1058 6700 x.emd"
img = hs.load(example_emd_file)

# %%
# Save in another format
# save as tifF:
img.save("example.tiff")
# save as png:
img.save("example.png")
# save as jpeg:
img.save("example.jpeg")
# %%
