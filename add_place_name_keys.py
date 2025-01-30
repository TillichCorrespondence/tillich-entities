import os
from acdh_tei_pyutils.tei import TeiReader
from acdh_tei_pyutils.utils import get_xmlid
from acdh_xml_pyutils.xml import NSMAP


data_dir = os.path.join("data", "indices")
listperson_file = os.path.join(data_dir, "listperson.xml")
listplace_file = os.path.join(data_dir, "listplace.xml")

lookup_dict = {}
doc = TeiReader(listplace_file)
for x in doc.any_xpath(".//tei:place[@xml:id]"):
    xmlid = get_xmlid(x)
    label = x.xpath("./tei:placeName[1]", namespaces=NSMAP)[0].text
    if label:
        lookup_dict[label.strip()] = xmlid
    else:
        x.getparent().remove(x)
doc.tree_to_file(listplace_file)

doc = TeiReader(listperson_file)
no_match = set()
for x in doc.any_xpath(".//tei:person//tei:placeName"):
    label = x.text
    try:
        key = lookup_dict[label.strip()]
        print(key)
    except KeyError:
        no_match.add(label)
        continue
    x.attrib["key"] = f"#{key}"
doc.tree_to_file(listperson_file)

with open("places_no_match.txt", "w", encoding="utf-8") as f:
    for x in no_match:
        f.write(f"{x}\n")
