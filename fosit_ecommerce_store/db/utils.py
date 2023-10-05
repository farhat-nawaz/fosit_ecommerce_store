from tortoise import Tortoise, connections
from yarl import URL

from fosit_ecommerce_store.settings import settings


async def create_database() -> None:
    db_url = URL.build(
        scheme="mysql",
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_pass,
        path="/sys",
    )

    await Tortoise.init(db_url=str(db_url), modules={"models": ["aerich.models"]})
    conn = connections.get("default")
    await conn.execute_query(f"CREATE DATABASE IF NOT EXISTS {settings.db_name}")
    await conn.close()
