import os
import json
import zipfile

def unzip_and_load(zip_path: str, extract_to: str = "Data") -> list:
    """
    Unzips the ZIP archive, loads the JSON file inside, and returns a list of transactions.
    """
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        json_files = [f for f in zip_ref.namelist() if f.endswith('.json')]

    if not json_files:
        raise FileNotFoundError("No JSON file found inside the zip archive.")

    json_file_path = os.path.join(extract_to, json_files[0])
    
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Optionally delete the extracted JSON
    os.remove(json_file_path)

    print(f"✅ Loaded {len(data)} transactions from: {json_files[0]}")
    return data
