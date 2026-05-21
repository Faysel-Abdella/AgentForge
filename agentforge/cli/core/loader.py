import json

def load_test_file(file_path: str):
    file = open(file_path, "r")

    content = file.read()

    data = json.loads(content)

    return data
