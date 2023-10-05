from cli import async_typer, db

app = async_typer.AsyncTyper()
app.add_typer(db.app, name="db")

if __name__ == "__main__":
    app()
