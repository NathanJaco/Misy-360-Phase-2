import streamlit as st
from services import product_service

def employee_dashboard_render():
    products = st.session_state["products"]
    user = st.session_state["user"]
    role = st.session_state["role"]

    col1, col2, col3 = st.columns([2, 3, 2])

    with col2:
        st.header("Employee Dashboard")

    st.divider()

    col1, col2 = st.columns([3, 2])

    with col1:
        with st.container(border=True):
            st.markdown("### Inventory")
            search_product = st.text_input("Search Product", key="search_product_txt")

            filtered_products = product_service.filter_products(products, search_product)

            if len(filtered_products) > 0:
                st.dataframe(filtered_products, use_container_width=True)
            else:
                st.info("No matching products found.")

        with st.container(border=True):
            st.markdown("### Low Stock Items")

            low_stock_products = product_service.get_low_stock_products(products)

            if len(low_stock_products) > 0:
                st.dataframe(low_stock_products, use_container_width=True)
            else:
                st.info("No low stock items found.")

    with col2:
        with st.container(border=True):
            st.markdown("### Logged In User")
            if user is not None:
                st.markdown(f"Email: {user['email']}")
                st.markdown(f"Role: {role}")