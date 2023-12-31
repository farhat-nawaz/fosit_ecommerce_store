from typing import List

from fosit_ecommerce_store.settings import settings

MODELS_MODULES: List[str] = [
    "fosit_ecommerce_store.db.models.inventory",
    "fosit_ecommerce_store.db.models.sales",
]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
