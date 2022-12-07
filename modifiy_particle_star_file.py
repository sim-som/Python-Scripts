#%%
from pathlib import Path
from starparser import fileparser
import pandas as pd
# %%
part_starfile = Path(
    "/u3/data/simon/image_data/cryoem_data/arctica/20221129_SiSo_Ins_Fib_Fractions/Extract/job006/particles.star"
)

# %%
particles, metadata = fileparser.getparticles(str(part_starfile))

# %%
test_str = particles.loc[0, "_rlnMicrographName"]
test_str

# %%
def mod_micrographname(name:str):

    correct_name = name.replace("average/", "../../average/")

    return correct_name

mod_micrographname(test_str)
# %%
particles._rlnMicrographName = particles._rlnMicrographName.apply(mod_micrographname)
particles
# %%
# Save cleaned particle-.star file:
dest_loc = part_starfile.parent / Path("processed-particles.star")
fileparser.writestar(particles, metadata, str(dest_loc))