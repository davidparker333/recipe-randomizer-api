from app import create_app
from scheduled import test

app = create_app()

@app.cli.command()
def scheduled():
    test()