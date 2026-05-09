import streamlit as st
from services import product_service

def employee_dashboard_render():
    products = st.session_state["products"]
    user = st.session_state["user"]
    role = st.session_state["role"]

    st.header("Employee Dashboard")
    st.caption("Search inventory and review low stock items.")
    st.divider()

    total_products = len(products)
    low_stock_products = product_service.get_low_stock_products(products)
    categories = product_service.get_categories(products)

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric("Total Products", total_products)

    with metric_col2:
        st.metric("Low Stock Items", len(low_stock_products))

    with metric_col3:
        st.metric("Categories", len(categories))

    st.divider()

    col1, col2 = st.columns([3, 2])

    with col1:
        with st.container(border=True):
            st.markdown("### Inventory Search")
            search_product = st.text_input("Search Product", key="search_product_txt")

            filtered_products = product_service.filter_products(products, search_product)

            if len(filtered_products) > 0:
                st.dataframe(filtered_products, use_container_width=True)
            else:
                st.info("No matching products found.")

        with st.container(border=True):
            st.markdown("### Low Stock Items")

            if len(low_stock_products) > 0:
                st.dataframe(low_stock_products, use_container_width=True)
            else:
                st.info("No low stock items found.")

    with col2:
        with st.container(border=True):
            st.markdown("### Employee Tools")
            st.markdown("- Search current inventory")
            st.markdown("- Review low stock items")
            st.markdown("- Check product categories")

        with st.container(border=True):
            st.markdown("### Logged In User")
            if user is not None:
                st.markdown(f"Email: {user['email']}")
                st.markdown(f"Role: {role}")