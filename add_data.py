# import requests
# from config import br_client, BASEROW_DB_ID
# from acdh_tei_pyutils.tei import TeiReader
# from tqdm import tqdm

# person_table_id = br_client.get_table_by_name(BASEROW_DB_ID, "persons")


# doc = TeiReader(
#     "https://raw.githubusercontent.com/TillichCorrespondence/tillich-briefe-data/main/data/indices/listperson.xml"
# )
# nsmap = doc.nsmap

# update_object = {}
# for x in tqdm(doc.any_xpath(".//tei:person")):

#     xml_id = x.attrib["{http://www.w3.org/XML/1998/namespace}id"]
#     baserow_id = xml_id.split("__")[-1]
#     update_url = f"{br_client.br_base_url}database/rows/table/{person_table_id}/{baserow_id}/?user_field_names=true"
#     try:
#         gnd = x.xpath("./tei:idno[@type='gnd']/text()", namespaces=nsmap)[0]
#     except IndexError:
#         gnd = "k."
#     if not "k." in gnd:
#         update_object["gnd_url"] = f"https://d-nb.info/gnd/{gnd}"

#     occupation = ""
#     for o in x.xpath(".//tei:occupation", namespaces=nsmap):
#         occupation += o.text
#     update_object["occupation"] = occupation
#     r = requests.patch(
#         update_url,
#         headers={
#             "Authorization": f"Token {br_client.br_token}",
#             "Content-Type": "application/json",
#         },
#         json=update_object,
#     )
