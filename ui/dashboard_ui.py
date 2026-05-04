import streamlit as st
from services import product_service

def owner_dashboard_render():
    products = st.session_state["products"]
    user = st.session_state["user"]
    role = st.session_state["role"]

    col1, col2, col3 = st.columns([2, 3, 2])

    with col2:
        st.header("Owner Dashboard")

    st.divider()

    total_products = len(products)
    low_stock = product_service.get_low_stock_products(products)
    categories = product_service.get_categories(products)

    col1, col2 = st.columns([3, 2])

    with col1:
        with st.container(border=True):
            st.markdown("### Inventory Summary")
            st.markdown(f"Total Products: {total_products}")
            st.markdown(f"Low Stock Items: {len(low_stock)}")
            st.markdown(f"Categories: {len(categories)}")

        with st.container(border=True):
            st.markdown("### Low Stock Alert")

            if len(low_stock) > 0:
                st.dataframe(low_stock, use_container_width=True)
            else:
                st.info("No low stock items.")

    with col2:
        with st.container(border=True):
            st.markdown("### Owner Actions")
            st.markdown("- Add new products")
            st.markdown("- Update product price")
            st.markdown("- Update product stock")
            st.markdown("- Delete products")

        with st.container(border=True):
            st.markdown("### Logged In User")
            if user is not None:
                st.markdown(f"Email: {user['email']}")
                st.markdown(f"Role: {role}")