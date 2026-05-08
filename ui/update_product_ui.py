import streamlit as st
from data.data_manager import DataManager
from services import product_service


def update_product_render():
    products = st.session_state["products"]
    product_manager = DataManager("products.json")

    st.header("Update Product")
    st.caption("Select a product and update its price or stock.")
    st.divider()

    with st.container(border=True):
        st.markdown("### Update Product Details")

        if len(products) == 0:
            st.info("No products available to update.")

        else:
            product_names = []

            for product in products:
                product_names.append(product["name"])

            selected_product = st.selectbox("Select Product", product_names)

            selected_product_data = None

            for product in products:
                if product["name"] == selected_product:
                    selected_product_data = product

            if selected_product_data is not None:
                st.markdown(f"**Category:** {selected_product_data['category']}")

                new_price = st.number_input(
                    "New Price",
                    min_value=0.0,
                    value=float(selected_product_data["price"]),
                    key=f"price_{selected_product}"
                )

                new_stock = st.number_input(
                    "New Stock",
                    min_value=0,
                    value=int(selected_product_data["stock"]),
                    key=f"stock_{selected_product}"
                )

                if st.button("Update", type="primary", use_container_width=True):
                    product_service.update_product(products, selected_product, new_price, new_stock)

                    product_manager.save_data(products)
                    st.session_state["products"] = products

                    st.success(f"{selected_product} updated successfully!")
                    st.rerun()