import requests
from tqdm import tqdm
from config import br_client, BASEROW_DB_ID
from acdh_geonames_utils.gn_client import gn_as_object
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri


place_table_id = br_client.get_table_by_name(BASEROW_DB_ID, "places")


items = []
filters = {"filter__field_24056__contains": "https", "filter__field_28262__empty": True}
for x in br_client.yield_rows(place_table_id, filters=filters):
    item = x
    items.append(item)
print(len(items))

for x in tqdm(items):
    update_object = {}
    update_url = f"{br_client.br_base_url}database/rows/table/{place_table_id}/{x['id']}/?user_field_names=true"
    try:
        gn_object = gn_as_object(x["geonames_url"])
    except Exception as e:
        print(e, update_url)
        continue
    update_object["latitude"] = gn_object["latitude"]
    update_object["longitude"] = gn_object["longitude"]
    update_object["geonames_url"] = get_normalized_uri(x["geonames_url"])
    r = requests.patch(
        update_url,
        headers={
            "Authorization": f"Token {br_client.br_token}",
            "Content-Type": "application/json",
        },
        json=update_object,
    )
    if int(r.status_code) != 200:
        print(r.status_code, x["name"])
