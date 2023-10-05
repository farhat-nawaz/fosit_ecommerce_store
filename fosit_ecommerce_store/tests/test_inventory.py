from typing import Any

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_add_categories(
    client: AsyncClient,
    fastapi_app: FastAPI,
    product_categories: dict[str, list[dict[str, str]]],
) -> None:
    """
    Checks the endpoint to add categories.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("add_product_categories")
    response = await client.post(url, json=product_categories)
    r: dict[str, Any] = response.json()

    assert r["status_code"] == status.HTTP_201_CREATED
    assert r["error"] == False  # noqa: E712
    assert r["message"] == "Operation successful!"


@pytest.mark.anyio
async def test_add_products(
    client: AsyncClient,
    fastapi_app: FastAPI,
    products_invalid: dict[Any, Any],
) -> None:
    """
    Checks the endpoint to add categories.

    :param client: client for the app.g
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("add_products")
    response = await client.post(url, json=products_invalid)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    r: dict[str, Any] = response.json()

    assert r["detail"][0]["msg"] == "Field required"
    assert r["detail"][0]["input"] == products_invalid
    assert r["detail"][0]["type"] == "missing"
