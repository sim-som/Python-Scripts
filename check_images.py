# %%
# imports
import argparse
import numpy as np
import mrcfile
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("agg")
from skimage import filters, exposure, io
from matplotlib_scalebar.scalebar import ScaleBar

# DIY modules
import sys
sys.path.insert(1, "C:/Users/simon/OneDrive/Dokumente/Studium/Master/Masterarbeit/Code/Metadata")
import metadata as meta

# %%
# Path to image files 
parser = argparse.ArgumentParser(
    description="""
        Plotting script to plot the powerspectrum and fitted ctf from the *avrot.txt
        files produced by CTFFIND4 (https://grigoriefflab.umassmed.edu/ctffind4)
    """
    )
parser.add_argument("img_dir_str", help="The directory where the results from ctffind4 reside")
args = parser.parse_args()
img_dir = Path(args.img_dir_str)
# img_dir = Path(r"c:\Users\simon\OneDrive\Bilder\Bilder-Masterarbeit\Talos_L120C\16-02-2022-GPCR_lipid_nanodisk_neg_stain_UA2_perc\8B-Gridbox226723-GPCR_lipid_nanodisk")
assert img_dir.exists() and img_dir.is_dir()

#%%
for img_p in img_dir.glob("*.tif"):
    print("Working on ", img_p.name, "...")

    png_file_path = img_dir / Path(f"{img_p.stem}.png")
    if png_file_path.exists():
        print("File already exists. Continuing with next image ...")
        continue

    if img_p.suffix == ".mrc":
        with mrcfile.open(img_p) as f:
            img = f.data
    else:
        img = io.imread(img_p)

    # simple denoising
    img = filters.median(img)

    # contrast stretching:
    p2, p98 = np.percentile(img, (2, 98))
    img = exposure.rescale_intensity(img, in_range=(p2, p98))

    # metadata:
    img_metadata = meta.get_file_metadata(img_p)
    px_size = meta.get_pixel_size_meter(img_metadata)



    fig, ax = plt.subplots()

    ax.axis("off")

    # Plot image:
    ax.imshow(img, cmap="gray")

    # Create scale bar
    scalebar = ScaleBar(
        px_size* 1e6, "µm",
        length_fraction=0.25,
        frameon=True,
        location="lower left",
        # color="white"
    )
    ax.add_artist(scalebar)

    plt.savefig(png_file_path, bbox_inches = "tight", dpi=300 * 3)
    
    # plt.show(block=True)

    plt.close()
# %%
