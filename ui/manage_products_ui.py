import streamlit as st
from data.data_manager import DataManager
from services import product_service

def manage_products_render():
    products = st.session_state["products"]
    product_manager = DataManager("products.json")

    st.header("Manage Products")
    st.divider()

    with st.container(border=True):
        st.markdown("### Product Management")

        if len(products) == 0:
            st.info("No products available.")

        else:
            for product in products:
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"**{product['name']}**")
                    st.caption(f"Category: {product['category']}")
                    st.markdown(f"Price: ${product['price']}")
                    st.markdown(f"Stock: {product['stock']}")
                    st.divider()

                with col2:
                    if st.button("Delete", key=product["name"]):
                        products = product_service.delete_product(products, product["name"])

                        product_manager.save_data(products)
                        st.session_state["products"] = products

                        st.success("Product deleted successfully!")
                        st.rerun()