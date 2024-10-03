from collections import defaultdict
from acdh_tei_pyutils.tei import TeiReader
from acdh_xml_pyutils.xml import NSMAP
from acdh_tei_pyutils.utils import make_entity_label, get_xmlid


nsmap = NSMAP

doc = TeiReader("data/indices/listperson.xml")
d = defaultdict(list)
for x in doc.any_xpath(".//tei:person[.//tei:idno[@type='gnd']]"):
    label = make_entity_label(x.xpath("./tei:persName", namespaces=nsmap)[0])[0]
    gnd_id = x.xpath(".//tei:idno[@type='gnd']/text()", namespaces=nsmap)[0]
    xml_id = get_xmlid(x)
    d[gnd_id].append([label, xml_id])
for key, value in d.items():
    if len(value) > 1:
        print(key, *value)

doc = TeiReader("data/indices/listplace.xml")
d = defaultdict(list)
for x in doc.any_xpath(".//tei:place[.//tei:idno[@type='geonames']]"):
    label = make_entity_label(x.xpath("./tei:placeName", namespaces=nsmap)[0])[0]
    gnd_id = x.xpath(".//tei:idno[@type='geonames']/text()", namespaces=nsmap)[0]
    xml_id = get_xmlid(x)
    d[gnd_id].append([label, xml_id])
for key, value in d.items():
    if len(value) > 1:
        print(key, *value)
