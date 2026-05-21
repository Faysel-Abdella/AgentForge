import json
from pathlib import Path

# Load multiple files
def load_test_files(path: str):
    
    test_files = []
    
    path_object = Path(path)
    
    # A single file
    if path_object.is_file():
        return [str(path_object)]
    
    # Folder
    for file in path_object.glob("*.json"):
        test_files.append(str(file))
    

def load_test_file(file_path: str):
    file = open(file_path, "r")

    content = file.read()

    data = json.loads(content)

    return data
