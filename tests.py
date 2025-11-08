import pytest
from db.queries import (
    get_all_products, add_product, update_product, delete_product,
    get_inventory, add_inventory, update_inventory, get_low_stock
)

TEST_SKU = "TEST123"

def test_add_and_get_product():
    add_product(TEST_SKU, "Test Widget", "Test Description", 5)
    products = get_all_products()
    assert any(p[0] == TEST_SKU for p in products)

def test_update_product():
    update_product(TEST_SKU, "Updated Widget", "Updated Desc", 3)
    products = get_all_products()
    updated = next((p for p in products if p[0] == TEST_SKU), None)
    assert updated is not None
    assert updated[1] == "Updated Widget"
    assert updated[2] == "Updated Desc"
    assert updated[3] == 3

def test_add_and_update_inventory():
    add_inventory(TEST_SKU, "Test Warehouse", 10)
    inventory = get_inventory()
    assert any(i[1] == TEST_SKU and i[2] == "Test Warehouse" for i in inventory)

    update_inventory(TEST_SKU, "Test Warehouse", 2)
    inventory = get_inventory()
    updated = next((i for i in inventory if i[1] == TEST_SKU and i[2] == "Test Warehouse"), None)
    assert updated is not None
    assert updated[3] == 2  # quantity

def test_low_stock_alert():
    low_stock = get_low_stock()
    assert any(i[0] == TEST_SKU for i in low_stock)

def test_delete_product():
    delete_product(TEST_SKU)
    products = get_all_products()
    assert all(p[0] != TEST_SKU for p in products)
