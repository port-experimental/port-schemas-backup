import os
import requests
import json
import tempfile
import shutil
from pathlib import Path

PORT_API_BASE = "https://api.getport.io/v1"
CLIENT_ID = os.environ.get("PORT_CLIENT_ID")
CLIENT_SECRET = os.environ.get("PORT_CLIENT_SECRET")
HEADERS = {"Content-Type": "application/json"}
TEMP = tempfile.gettempdir()
ENDPOINTS = ["blueprints", "actions", "scorecards"]  # the Port API endpoints to backup


def create_tmp_backup_folder():
    folder = f"{Path(tempfile.gettempdir())}/port-backup"
    os.makedirs(folder, exist_ok=True)
    return folder


def authenticate():
    url = f"{PORT_API_BASE}/auth/access_token"
    data = {"clientId": CLIENT_ID, "clientSecret": CLIENT_SECRET}
    resp = requests.post(url, json=data, headers=HEADERS)
    resp.raise_for_status()
    token = resp.json()["accessToken"]
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def get_all(endpoint, headers):
    url = f"{PORT_API_BASE}/{endpoint}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def parse_endpoint(response, endpoint, tmpfolder):
    folder = f"{Path(tmpfolder)/endpoint}"
    print(f"Creating folder: {folder}")
    os.makedirs(folder, exist_ok=True)
    print(f"Saving {endpoint} data to {folder}")
    for schema in response[endpoint]:
        try:
            save_json(schema, f"{folder}/{schema['identifier']}.json")
        except Exception as e:
            print(
                f"Error saving {endpoint} with identifier {schema.get('identifier', 'unknown')}: {e}"
            )


def backup_port_schemas():
    headers = authenticate()
    endpoints = ENDPOINTS.copy()  # Add or remove endpoints as needed from ENDPOINTS
    tmp = create_tmp_backup_folder()
    print(f"Temporary backup folder created at: {tmp}")

    for endpoint in endpoints:
        print(f"Backing up {endpoint}...")
        response = get_all(endpoint, headers)
        parse_endpoint(response, endpoint, tmp)
    print("Zipping backup files...")
    base_name = "port-schemas-backup"
    zip_path = Path(f"{base_name}.zip")
    if not zip_path.exists():
        final_zip_path = zip_path
    else:
        count = 1
        while True:
            candidate = Path(f"{base_name} ({count}).zip")
            if not candidate.exists():
                final_zip_path = candidate
                break
            count += 1
    shutil.make_archive(final_zip_path.with_suffix("").as_posix(), "zip", tmp) # create zip archive
    shutil.rmtree(tmp) # clean up temporary folder


if __name__ == "__main__":
    print("Backing Up Port Schemas...")
    backup_port_schemas()
    print("Backup completed successfully.")
