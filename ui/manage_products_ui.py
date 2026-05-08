import streamlit as st
from data.data_manager import DataManager
from services import product_service

def manage_products_render():
    products = st.session_state["products"]
    product_manager = DataManager("products.json")

    if "confirm_delete_product" not in st.session_state:
        st.session_state["confirm_delete_product"] = None

    st.header("Manage Products")
    st.caption("View, edit, or remove products from the inventory.")
    st.divider()

    with st.container(border=True):
        st.markdown("### Product Management")

        if len(products) == 0:
            st.info("No products available.")

        else:
            for product in products:
                col1, col2, col3 = st.columns([4, 1, 1])

                with col1:
                    st.markdown(f"**{product['name']}**")
                    st.caption(f"Category: {product['category']}")
                    st.markdown(f"Price: ${product['price']}")
                    st.markdown(f"Stock: {product['stock']}")

                with col2:
                    if st.button("Edit", key=f"edit_{product['name']}"):
                        st.session_state["page"] = "update_product"
                        st.rerun()

                with col3:
                    if st.button("Delete", key=f"delete_{product['name']}"):
                        st.session_state["confirm_delete_product"] = product["name"]
                        st.rerun()

                if st.session_state["confirm_delete_product"] == product["name"]:
                    st.warning(f"Are you sure you want to delete {product['name']}?")

                    confirm_col1, confirm_col2 = st.columns(2)

                    with confirm_col1:
                        if st.button("Confirm Delete", key=f"confirm_delete_{product['name']}", type="primary"):
                            products = product_service.delete_product(products, product["name"])

                            product_manager.save_data(products)
                            st.session_state["products"] = products
                            st.session_state["confirm_delete_product"] = None

                            st.success("Product deleted successfully!")
                            st.rerun()

                    with confirm_col2:
                        if st.button("Cancel", key=f"cancel_delete_{product['name']}"):
                            st.session_state["confirm_delete_product"] = None
                            st.rerun()

                st.divider()