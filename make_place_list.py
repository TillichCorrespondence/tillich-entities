import pandas as pd
import glob

from acdh_tei_pyutils.tei import TeiReader

doc = TeiReader(
    "https://raw.githubusercontent.com/TillichCorrespondence/tillich-briefe-data/main/data/indices/listperson.xml"
)
nsmap = doc.nsmap


items = list()
faulty = list()
for x in doc.any_xpath(".//tei:placeName/text()"):
    items.append(x)

for x in glob.glob("../TillichEdition/data/*.xml"):
    try:
        doc = TeiReader(x)
    except Exception as e:
        faulty.append([x, e])
    for p in doc.any_xpath(".//tei:placeName[@ref]/@ref"):
        items.append(p)

for x in glob.glob("../TillichEdition/Data_unrefined/*.xml"):
    try:
        doc = TeiReader(x)
    except Exception as e:
        faulty.append([x, e])
    for p in doc.any_xpath(".//tei:placeName[@ref]/@ref"):
        items.append(p)
print(len(items))
print(len(set(items)))
print(faulty)

data = []
for i, x in enumerate(sorted(set(items)), 1):
    tillich_id = f"tillich_place_id__{i}"
    item = {"name": x, "tillich_id": tillich_id, "geonames_url": ""}
    data.append(item)

df = pd.DataFrame(data)

df.to_csv("places.csv", index=False)
