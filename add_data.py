import requests
from config import br_client, BASEROW_DB_ID
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm

person_table_id = br_client.get_table_by_name(BASEROW_DB_ID, "persons")


doc = TeiReader(
    "https://raw.githubusercontent.com/TillichCorrespondence/tillich-briefe-data/main/data/indices/listperson.xml"
)
nsmap = doc.nsmap

update_objects = {
    "items": []
}
for x in tqdm(doc.any_xpath(".//tei:person")):
    xml_id = x.attrib["{http://www.w3.org/XML/1998/namespace}id"]
    baserow_id = xml_id.split("__")[-1]
    item = {
        "id": baserow_id
    }
    try:
        node = x.xpath("./tei:note[@type='bio']", namespaces=nsmap)[0]
        item["bio"] = " ".join(''.join(node.itertext()).split())
    except IndexError:
        item["bio"] = ""
    update_objects["items"].append(item)

update_url = f"{br_client.br_base_url}database/rows/table/{person_table_id}/batch/?user_field_names=true"

r = requests.patch(
    update_url,
    headers={
        "Authorization": f"Token {br_client.br_token}",
        "Content-Type": "application/json",
    },
    json=update_objects,
)
print(update_objects)
print(r)
