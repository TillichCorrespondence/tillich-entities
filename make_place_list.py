import pandas as pd
import glob

from acdh_tei_pyutils.tei import TeiReader

doc = TeiReader(
    "https://raw.githubusercontent.com/TillichCorrespondence/tillich-briefe-data/main/data/indices/listperson.xml"
)
nsmap = doc.nsmap


items = list()
for x in doc.any_xpath(".//tei:placeName/text()"):
    items.append(x)

for x in glob.glob("../TillichEdition/data/*.xml"):
    doc = TeiReader(x)
    for p in doc.any_xpath(".//tei:placeName[@ref]/@ref"):
        items.append(p)
print(len(items))
print(len(set(items)))

data = []
for i, x in enumerate(sorted(set(items)), 1):
    tillich_id = f"tillich_place_id__{i}"
    data.append({"name": x, "tillich_id": tillich_id})

df = pd.DataFrame(data)

df.to_csv("places.csv", index=False)
