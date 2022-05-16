#%%
# imports
from hyperspy import api as hs
import hyperspy
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar

# %%
# Load the image data via hyperspy :
emd_file_p = Path("C:/Users/simon/OneDrive/Desktop/B2-Empty_glow_dis_quantifoil 20220127 1313 6700 x.emd")
img_signal = hs.load(emd_file_p)

img_signal.plot()

# %%
# Save in another format
# save as tiff:
# img.save("example.tiff")
# save as png:
# img_signal.save("example.png")
# save as jpeg:
# img.save("example.jpeg")
# %%
# Get the image data as a numpy array:
img = img_signal.data
# Get the metadata as tree:
metadata = img_signal.original_metadata

# %%
# pixel size:
def get_px_size(metadata:hyperspy.misc.utils.DictionaryTreeBrowser):
    """Get the pixel size in meter from a hyperspy generated metadata tree.

    Args:
        metadata (hyperspy.misc.utils.DictionaryTreeBrowser): Metadata of the image signal class in hyperspy
    """

    px_size_dict = metadata.BinaryResult.PixelSize

    if px_size_dict["height"] == px_size_dict["width"]:
        return float(px_size_dict["height"])
    else:
        print("Pixel shape not quadratic !!!")
        return (px_size_dict["height"], px_size_dict["width"])

px_size = get_px_size(metadata)

# %%
# filter the image:
from skimage.filters import median
img_proc = median(img)

plt.figure(figsize=(12,6))

plt.subplot(121)
plt.imshow(img, cmap="gray")
plt.title("raw image")

plt.subplot(122)
plt.imshow(img_proc, cmap="gray")
plt.title("median filterd image")

plt.show()

# %%
# Plot image with scalebar:

# Create subplot
fig, ax = plt.subplots(figsize=(6,6))
ax.axis("off")

# Plot image
ax.imshow(img_proc, cmap="gray")

# Create scale bar
scalebar = ScaleBar(
    px_size,
    units = "m", 
    length_fraction = 0.2,
    location="lower left",
    box_alpha=0.0

)
ax.add_artist(scalebar)

# Show
plt.show()

# %%
# Save the figure of the image together with the scalebar as .png
output_p = emd_file_p.parent / Path(f"{emd_file_p.stem}.png")
print(f"Saving as png with scalebar to {output_p} ")

fig.savefig(
    output_p,
    dpi = 500,
    bbox_inches = "tight",
    pad_inches = 0
)
# %%
