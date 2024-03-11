import requests
import json
from tqdm import tqdm
from config import br_client, BASEROW_DB_ID

persons_table = br_client.get_table_by_name(BASEROW_DB_ID, "persons")

with open("mycache/gnd_persons.json", "r") as f:
    gnd_persons = json.load(f)

cleaned_gnd_persons = {}
for key, value in gnd_persons.items():
    cleaned_gnd_persons[key] = {}
    try:
        cleaned_gnd_persons[key]["date_of_birth"] = value["dateOfBirth"][0]
    except (KeyError, IndexError):
        cleaned_gnd_persons[key]["date_of_birth"] = ""
    try:
        cleaned_gnd_persons[key]["date_of_death"] = value["dateOfDeath"][0]
    except (KeyError, IndexError):
        cleaned_gnd_persons[key]["date_of_death"] = ""
    try:
        cleaned_gnd_persons[key]["place_of_birth"] = value["placeOfBirth"][0]["label"]
    except (KeyError, IndexError):
        cleaned_gnd_persons[key]["place_of_birth"] = ""
    try:
        cleaned_gnd_persons[key]["place_of_death"] = value["placeOfDeath"][0]["label"]
    except (KeyError, IndexError):
        cleaned_gnd_persons[key]["place_of_death"] = ""

for key, value in tqdm(cleaned_gnd_persons.items()):
    update_object = {}
    update_url = f"{br_client.br_base_url}database/rows/table/{persons_table}/{key}/?user_field_names=true"
    print(update_url)
    r = requests.patch(
        update_url,
        headers={
            "Authorization": f"Token {br_client.br_token}",
            "Content-Type": "application/json",
        },
        json=value,
    )
    if int(r.status_code) != 200:
        print(r.status_code, value)