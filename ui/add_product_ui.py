import streamlit as st
from data.data_manager import DataManager


def add_product_render():
    products = st.session_state["products"]
    product_manager = DataManager("products.json")

    st.header("Add Product")
    st.divider()

    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        with st.container(border=True):
            st.markdown("### Add Product Form")

            product_name = st.text_input("Product Name", key="product_name_input")
            category = st.text_input("Category", key="category_input")
            price = st.number_input("Price", min_value=0.0, step=0.5, key="price_input")
            stock = st.number_input("Stock", min_value=0, step=1, key="stock_input")

            if st.button("Save Product", key="save_product_btn", type="primary", use_container_width=True):
                product_exists = False

                for product in products:
                    if product["name"].lower() == product_name.lower():
                        product_exists = True

                if not product_name or not category:
                    st.warning("Please complete all fields")

                elif product_exists:
                    st.error("A product with that name already exists")

                else:
                    products.append(
                        {
                            "name": product_name,
                            "category": category,
                            "price": price,
                            "stock": stock
                        }
                    )

                    product_manager.save_data(products)
                    st.session_state["products"] = products

                    st.success("Product saved successfully!")
                    st.rerun()