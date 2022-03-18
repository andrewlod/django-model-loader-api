from uuid import uuid4
import os
import zipfile
from .. import constants
from django.core.files.storage import default_storage

def store_file(file, storage_type, file_id=None):
    if file_id == None:
        file_id = str(uuid4())
    
    storage_type_id = constants.STORAGE_TYPES[storage_type]

    if storage_type == "AWS":
        default_storage.save(file_id, file)
    elif storage_type == "Local":
        pass
    else:
        return False

    return file_id, storage_type_id

def download_and_extract(file_id):
    data = default_storage.open(file_id).read()
    
    directory = f"temp/{file_id}"
    os.makedirs(directory, exist_ok=True)
    path = directory + ".zip"

    with open(path, 'wb+') as file:
        file.write(data)
        file.close()
    
    with zipfile.ZipFile(path, 'r') as zipped:
        zipped.extractall(directory)
    
    os.remove(path)
    
    return directory


def download_file(file_id):
    data = default_storage.open(file_id).read()
    
    path = f"temp/{file_id}"

    with open(path, 'wb+') as file:
        file.write(data)
        file.close()
    
    return path


def read_file(file_id):
    return default_storage.open(file_id).read()