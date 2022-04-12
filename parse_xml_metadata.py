#%%
# Imports
from bs4 import BeautifulSoup as bs
from pathlib import Path
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
# %%
xml_file = Path("/home/simon/jureca_project_mount/20220307_GPCR_nanodisk_Simon/FoilHole_8536003_Data_6461108_6461110_20220309_164658_fractions.xml")
assert xml_file.exists() and xml_file.is_file()

# %%
# Read xml_file as string:
with open(xml_file, encoding="utf-16") as f:    # Warum auch immer utf-16 statt utf-8
    print("Hello")
    xml_content = f.read()
# %%
# parsing with bs4:
soup = bs(xml_content, "html.parser")
print(soup.prettify())
# %%
for param in soup.find_all("param"):
    #print(param)
    name = param.get("name")
    val = param.get("value")
    if "defocus" in name.lower():
        print(name, val)
    if "pixel" in name.lower() or "pixelsize" in name.lower():
        print(name, val)
# %%
def search(param:str, soup):
    matches = {}
    for p in soup.find_all("param"):
        name = p.get("name")
        val = p.get("value")
        if param.strip().lower() in name.lower():
            matches[name] = val
    return matches
# %%
# iterate over all xml-files in the directory:
defocus_vals = []
dir = xml_file.parent
for xml_file in dir.glob("*.xml"):
    print("parsing", xml_file.name, "...")
    with open(xml_file, encoding="utf-16") as f:    # Warum auch immer utf-16 statt utf-8
        xml_content = f.read()
    # parsing with bs4:
    soup = bs(xml_content, "html.parser")
    defocus_vals.append(search("Defocus", soup))
# %%
defocus_df = pd.DataFrame(defocus_vals)
#%%
defocus_df = defocus_df.astype(float)
# %%
plt.plot(defocus_df["Defocus"])
# %%
plt.figure(figsize=(12,6))

plt.subplot(211)
sns.histplot(data=defocus_df, x="Defocus")

plt.subplot(212)
plt.plot(defocus_df.Defocus, ".")
plt.xlabel("image ID")
plt.ylabel("Fitted Defocus / $\mu$m")
plt.suptitle("WARPs CTF estimation")
# %%
# Pixel size:
# iterate over all xml-files in the directory:
pixelsize_vals = []
dir = xml_file.parent
for xml_file in dir.glob("*.xml"):
    print("parsing", xml_file.name, "...")
    with open(xml_file, encoding="utf-16") as f:    # Warum auch immer utf-16 statt utf-8
        xml_content = f.read()
    # parsing with bs4:
    soup = bs(xml_content, "html.parser")
    pixelsize_vals.append(search("pixelsize", soup))
# %%
pixelsize_df = pd.DataFrame(pixelsize_vals)
# %%
pixelsize_df = pixelsize_df.astype(float)
#%%
del pixelsize_df["PixelSizeDeltaPercent"]
# %%
pixelsize_df.boxplot()
# %%
