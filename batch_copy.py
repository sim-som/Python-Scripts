# %%
from pathlib import Path
import os
import shutil

text_file_p = Path("/run/user/1009/gvfs/smb-share:server=134.94.166.192,share=transfer/Gunnar_out/200916-trehalose-tmv/treh-tmv/selected_files_for_SPA.txt")
# set text files parent dir to working dir of the script:
os.chdir(text_file_p.parent)
# iterate over all selected image file names:
with open(text_file_p, encoding="utf-8") as f:
    for row in f:
        fname = row.strip()
        print("Copying", fname, "...")
        img_file_p = Path.cwd() / Path(fname)
        dst = Path("to_jureca") / Path(img_file_p.name)
        assert img_file_p.exists()
        shutil.copyfile(img_file_p, dst)