import typer

app = typer.Typer()

@app.command()
def test():
    print("This is test")
    
if __name__ == "__main__":
    app()