#%%
# imports
from hyperspy import api as hs
import hyperspy
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
import argparse

# %%
# Path to image file
parser = argparse.ArgumentParser(
    description="""
        Read in .emd files via hyperspy module add a salebar and save figure of image and overlaid scalebar as .png
    """
)

parser.add_argument("emd_file_str", help="The path of the .emd file")
parser.add_argument("--color", help="The color of the scalebar", default="black", type=str)
parser.add_argument("--box_alpha", help="Transparency of the box around the scalebar (range: [0.0, 1.0])",
                    default=0.0, type=float)
parser.add_argument("--verbose", action="store_true")

args = parser.parse_args()
emd_file_p = Path(args.emd_file_str)
# Load the image data via hyperspy :
img_signal = hs.load(emd_file_p)

# img_signal.plot()
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

plt.figure(emd_file_p.name ,figsize=(12,6))

plt.subplot(121)
plt.imshow(img, cmap="gray")
plt.title("raw image")

plt.subplot(122)
plt.imshow(img_proc, cmap="gray")
plt.title("median filterd image")

if args.verbose:
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
    color=args.color,
    length_fraction = 0.2,
    location="lower left",
    box_alpha=args.box_alpha

)
ax.add_artist(scalebar)

if args.verbose:
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
