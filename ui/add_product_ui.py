import streamlit as st
from data.data_manager import DataManager
from services import product_service

def add_product_render():
    products = st.session_state["products"]
    product_manager = DataManager("products.json")

    st.header("Add Product")
    st.caption("Add a new product to the inventory using the form below.")
    st.divider()

    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        with st.container(border=True):
            st.markdown("### Add Product Form")

            product_name = st.text_input("Product Name", key="product_name_input")

            category = st.selectbox(
                "Category",
                ["School Supplies", "Office", "Technology", "Food", "Other"],
                key="category_input"
            )

            price = st.number_input("Price", min_value=0.0, step=0.5, key="price_input")
            stock = st.number_input("Stock", min_value=0, step=1, key="stock_input")

            if st.button("Save Product", key="save_product_btn", type="primary", use_container_width=True):
                product_exists = product_service.product_exists(products, product_name)

                if not product_name:
                    st.warning("Please enter a product name.")

                elif product_exists:
                    st.error("A product with that name already exists.")

                else:
                    product_service.add_product(products, product_name, category, price, stock)

                    product_manager.save_data(products)
                    st.session_state["products"] = products

                    st.success(f"{product_name} was saved successfully.")
                    st.info("The product has been added to the inventory list.")