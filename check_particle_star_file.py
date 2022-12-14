#%%
import pandas as pd
from starparser import fileparser
from pathlib import Path
# %%
part_star_f = Path(
    "/home/simon/jureca_scratch_mount/20221129_SiSo_Ins_Fib_Fractions/relion4_processing/Extract/job029/particles.star"
)

part_df, metadata = fileparser.getparticles(str(part_star_f))

# %%
part_df
# %%
part_df.info()
# %%
per_mic_part_dfs = part_df.groupby("_rlnMicrographName")
# %%
len(per_mic_part_dfs)
# %%
