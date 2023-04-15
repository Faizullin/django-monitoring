import os
from django.core.files.storage import default_storage

folder_path = 'uploads/user_1'

def get_folder_size(folder_path):
    total_size = 0
    print(folder_path,default_storage.listdir(folder_path))
    _, filenames = default_storage.listdir(folder_path)
    for f in filenames:
        fp = os.path.join(folder_path, f)
        total_size += default_storage.size(fp)
    return total_size

# Get the total size of the folder in MB
folder_size_mb = get_folder_size(folder_path)

print(f"Folder size: {folder_size_mb} MB")