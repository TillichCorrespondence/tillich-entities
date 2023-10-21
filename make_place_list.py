import pandas as pd
import glob

from acdh_tei_pyutils.tei import TeiReader

doc = TeiReader(
    "https://raw.githubusercontent.com/TillichCorrespondence/tillich-briefe-data/main/data/indices/listperson.xml"
)
nsmap = doc.nsmap


items = set()
for x in doc.any_xpath(".//tei:placeName/text()"):
    items.add(x)

for x in glob.glob("../tillich-briefe-data/data/editions/*.xml"):
    doc = TeiReader(x)
    for p in doc.any_xpath(".//tei:rs[@type='place' and @ref]/@ref"):
        items.add(p[1:])


data = []
for i, x in enumerate(sorted(items), 1):
    tillich_id = f"tillich_place_id__{i}"
    data.append({"name": x, "tillich_id": tillich_id})

df = pd.DataFrame(data)

df.to_csv("places.csv", index=False)
