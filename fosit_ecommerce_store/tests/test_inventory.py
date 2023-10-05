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
@pytest.mark.parametrize("test_input, expected", [({}, ("Field required", "missing"))])
async def test_add_products_error(
    client: AsyncClient,
    fastapi_app: FastAPI,
    test_input: dict[str, str],
    expected: tuple[str, str],
) -> None:
    """
    Checks the endpoint to add categories.

    :param client: client for the app.g
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("add_products")
    response = await client.post(url, json=test_input)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    r: dict[str, Any] = response.json()
    msg, error_type = expected

    assert r["detail"][0]["msg"] == msg
    assert r["detail"][0]["input"] == test_input
    assert r["detail"][0]["type"] == error_type


@pytest.mark.anyio
@pytest.mark.parametrize("expected", [(200, "Operation successful!", False)])
async def test_get_products(
    client: AsyncClient,
    fastapi_app: FastAPI,
    expected: tuple[int, str, bool],
) -> None:
    """
    Checks the endpoint to add categories.

    :param client: client for the app.g
    :param fastapi_app: current FastAPI application.
    """
    status_code, msg, error = expected
    url = fastapi_app.url_path_for("get_products")

    response = await client.get(url)

    assert response.status_code == status_code

    r: dict[str, Any] = response.json()

    assert r["message"] == msg
    assert r["error"] == error
