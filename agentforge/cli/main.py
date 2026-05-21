import typer
import json

app = typer.Typer()

@app.command()
def test(file_path: str):
    # STEP 1: open file
    file = open(file_path, "r")

    # STEP 2: read file content as text
    content = file.read()

    # STEP 3: convert JSON string → Python object
    data = json.loads(content)

    # STEP 4: print result
    print(data)

if __name__ == "__main__":
    app()
