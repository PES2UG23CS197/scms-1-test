import streamlit as st
import pandas as pd
from db.queries import (
    get_all_products, add_product, update_product, delete_product,
    add_inventory, update_inventory
)

st.title("Product Manager")

# --- Form State Reset ---
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

if st.session_state.form_submitted:
    st.session_state.update({
        "sku": "",
        "name": "",
        "desc": "",
        "threshold": 1,
        "location": "",
        "quantity": 0,
        "form_submitted": False
    })

# --- Unified Add/Update Form ---
st.subheader("Add or Update Product")
with st.form("product_form"):
    st.text_input("SKU", key="sku")
    st.text_input("Name", key="name")
    st.text_input("Description", key="desc")
    st.number_input("Threshold", min_value=1, key="threshold")
    st.text_input("Warehouse Location", key="location")
    st.number_input("Quantity", min_value=0, key="quantity")

    col1, col2 = st.columns([1, 1])
    with col1:
        add_clicked = st.form_submit_button("➕ Add Product")
    with col2:
        update_clicked = st.form_submit_button("✏️ Update Product")

# --- Action Logic ---
if add_clicked:
    add_product(st.session_state.sku, st.session_state.name, st.session_state.desc, st.session_state.threshold)
    add_inventory(st.session_state.sku, st.session_state.location, st.session_state.quantity)
    st.success(f"Product '{st.session_state.sku}' added with {st.session_state.quantity} units at {st.session_state.location}")
    st.session_state.form_submitted = True
    st.rerun()

if update_clicked:
    update_product(st.session_state.sku, st.session_state.name, st.session_state.desc, st.session_state.threshold)
    update_inventory(st.session_state.sku, st.session_state.location, st.session_state.quantity)
    st.info(f"Product '{st.session_state.sku}' updated successfully!")
    st.session_state.form_submitted = True
    st.rerun()

# --- Product List ---
st.subheader("All Products")

products = get_all_products()

if products:
    # Header row
    header = st.columns([1.5, 2.5, 3, 1.5, 1])
    header[0].markdown("**SKU**")
    header[1].markdown("**Name**")
    header[2].markdown("**Description**")
    header[3].markdown("**Threshold**")
    header[4].markdown("**Delete**")

    # Data rows
    for p in products:
        row = st.columns([1.5, 2.5, 3, 1.5, 1])
        row[0].write(p[0])  # SKU
        row[1].write(p[1])  # Name
        row[2].write(p[2])  # Description
        row[3].write(p[3])  # Threshold
        if row[4].button("🗑️", key=f"delete_{p[0]}"):
            delete_product(p[0])
            st.warning(f"Deleted {p[0]}")
            st.rerun()
else:
    st.info("No products found.")
