#%%
import numpy as np
import mrcfile
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
from skimage import exposure, morphology, draw
from skimage import img_as_ubyte
# %%
classes_mrc_stack_p = Path(
    "/home/simon/jureca_scratch_mount/20221129_SiSo_Ins_Fib_Fractions/relion4_processing/Select/job044/class_averages.mrcs"
)

with mrcfile.open(classes_mrc_stack_p) as mrc:
    classes = mrc.data

# %%
angpix = 0.816
boxsize = classes.shape[-1]
mask_diam = 0.9 * boxsize
# %%
for i in range(classes.shape[0]):
    plt.figure()
    plt.imshow(classes[i,:,:], cmap="gray")
    break
# %%
img = classes[0,:,:]
plt.imshow(img,cmap="gray")
plt.colorbar()
# %%
# Histogram
plt.hist(img.ravel(), bins="auto")
# %%
# recreate mask

def recreate_mask(img, mask_diam_fraction=0.9):
    assert img.shape[0] == img.shape[1]
    boxsize = img.shape[0]

    # mask = img == 0
    # mask = morphology.binary_closing(mask, morphology.disk(boxsize // 2))
    
    mask_diam = mask_diam_fraction * boxsize
    mask_rad = mask_diam // 2

    mask = np.ones_like(img, dtype=bool)

    rr, cc = draw.disk(
        center=(boxsize//2, boxsize//2),
        radius=mask_rad,
        shape=img.shape
    )
    mask[rr, cc] = False

    return mask

mask = recreate_mask(img)
plt.imshow(mask, cmap="gray")
plt.colorbar()
#%%
# rescale:
img_trans = img - img.min()
trans_max = img_trans.max()
img_resc = img_trans / trans_max

plt.imshow(img_resc, cmap="gray")
plt.colorbar()
plt.title("Rescaled to [0,1]")

#%%
# convert to 8bit int:
img_8bit = img_as_ubyte(img_resc)
plt.imshow(img_8bit, cmap="gray")
plt.colorbar()
plt.title("8bit version")


#%%
im = Image.fromarray(img_8bit)
im.show()
# %%

rgba_im = im.convert("RGBA")
rgba_im.show()
# %%
# make masked out pixels transparent
datas = rgba_im.getdata()
newData = []

flat_mask = mask.flatten()
for i, item in enumerate(datas):
    if flat_mask[i]:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

rgba_im.putdata(newData)
rgba_im.show()
# %%

def make_transparent_img(img:np.array):

    # recreate mask
    mask = recreate_mask(img)

    # rescale:
    img_trans = img - img.min()
    trans_max = img_trans.max()
    img_resc = img_trans / trans_max

    # convert to 8bit int:
    img_8bit = img_as_ubyte(img_resc)

    im = Image.fromarray(img_8bit)
    rgba_im = im.convert("RGBA")

    # make masked out pixels transparent
    datas = rgba_im.getdata()
    newData = []

    flat_mask = mask.flatten()
    for i, item in enumerate(datas):
        if flat_mask[i]:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    rgba_im.putdata(newData)

    return rgba_im

trans_im = make_transparent_img(img)
trans_im.show()



# %%
for i in range(classes.shape[0]):
    
    trans_im = make_transparent_img(classes[i,:,:])
    
    save_dest = Path("/home/simon/simon_data/OneDrive/Dokumente/Promotion/Auswertungen/Insulin_Fibrils/20221129_SiSo_Ins_Fib_Fractions-Class2D_job044") / f"{classes_mrc_stack_p.stem}_class{i}.png"
    trans_im.save(save_dest, "PNG")

# %%
