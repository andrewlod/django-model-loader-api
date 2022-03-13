from uuid import uuid4
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