from pathlib import Path

from cli.async_typer import AsyncTyper
from tortoise import Tortoise, connections

from fosit_ecommerce_store.db.config import TORTOISE_CONFIG

app = AsyncTyper()


@app.command()
async def load_sample_data():
    """
    This command loads sample data into the database using fosit_ecommerce_store.db.sql.sample_data.sql # noqa: E501
    file shipped with the project.
    """
    await Tortoise.init(TORTOISE_CONFIG)
    conn = connections.get("default")

    sql = None
    sql_file_url = Path.cwd() / "fosit_ecommerce_store/db/sql/sample_data.sql"

    print("\n")
    print(f"Reading `{sql_file_url}`")
    with open(sql_file_url, "r") as f:
        sql = f.read()

    print("Executing...")
    for query in sql.strip(";").split(";"):
        query = query.strip()
        if query:
            await conn.execute_query(query)
    print("Data load complete!")


if __name__ == "__main__":
    app()
