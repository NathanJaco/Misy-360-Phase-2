import streamlit as st
from data.data_manager import DataManager
from ui import dashboard_ui
from ui import inventory_ui
from ui import add_product_ui
from ui import manage_products_ui
from ui import update_product_ui
from ui import login_register_ui


st.set_page_config("Inventory Manager", layout="wide", initial_sidebar_state="expanded")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"


user_manager = DataManager("users.json")
product_manager = DataManager("products.json")

if "users" not in st.session_state:
    st.session_state["users"] = user_manager.load_data()

if "products" not in st.session_state:
    st.session_state["products"] = product_manager.load_data()


with st.sidebar:
    st.markdown("### Inventory Manager")

    if st.session_state["logged_in"] == False:
        if st.button("Login", key="login_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "login"
            st.rerun()

        if st.button("Register", key="register_btn", type="primary", use_container_width=True):
            st.session_state["page"] = "register"
            st.rerun()

    else:
        if st.session_state["role"] == "Owner":
            if st.button("Owner Dashboard", key="owner_dashboard_btn", type="primary", use_container_width=True):
                st.session_state["page"] = "owner_dashboard"
                st.rerun()

            if st.button("Add Product", key="add_product_btn", type="primary", use_container_width=True):
                st.session_state["page"] = "add_product"
                st.rerun()

            if st.button("Manage Products", key="manage_products_btn", type="primary", use_container_width=True):
                st.session_state["page"] = "manage_products"
                st.rerun()

            if st.button("Update Product", key="update_product_btn", use_container_width=True):
                st.session_state["page"] = "update_product"
                st.rerun()

            if st.button("Chatbot", key="chatbot_btn", use_container_width=True):
                st.session_state["page"] = "chatbot"
                st.rerun()

        elif st.session_state["role"] == "Employee":
            if st.button("Employee Dashboard", key="employee_dashboard_btn", type="primary", use_container_width=True):
                st.session_state["page"] = "employee_dashboard"
                st.rerun()

            if st.button("Chatbot", key="chatbot_emp_btn", use_container_width=True):
                st.session_state["page"] = "chatbot"
                st.rerun()

        if st.button("Log Out", key="logout_btn", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.session_state["role"] = None
            st.session_state["page"] = "login"
            st.rerun()


st.header("Small Business Inventory Manager")
st.divider()

if st.session_state["page"] == "login":
    login_register_ui.login_render()

elif st.session_state["page"] == "register":
    login_register_ui.register_render()

elif st.session_state["page"] == "owner_dashboard":
    dashboard_ui.owner_dashboard_render()

elif st.session_state["page"] == "employee_dashboard":
    inventory_ui.employee_dashboard_render()

elif st.session_state["page"] == "add_product":
    add_product_ui.add_product_render()

elif st.session_state["page"] == "manage_products":
    manage_products_ui.manage_products_render()

elif st.session_state["page"] == "update_product":
    update_product_ui.update_product_render()

elif st.session_state["page"] == "chatbot":
    st.header("Chatbot")
    st.caption("Ask questions about inventory, stock, categories, or product management.")
    st.divider()

    products = st.session_state["products"]

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi! How can I help you?"}
        ]

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Ask a question...")

    if user_input:
        st.session_state["messages"].append(
            {
                "role": "user",
                "content": user_input
            }
        )

        ai_response = ""

        if "low stock" in user_input.lower():
            low_stock = []

            for product in products:
                if product["stock"] < 5:
                    low_stock.append(product["name"])

            if len(low_stock) > 0:
                ai_response = "Low stock items: " + ", ".join(low_stock)
            else:
                ai_response = "All items have sufficient stock."

        elif "total products" in user_input.lower():
            ai_response = f"There are {len(products)} products in the inventory."

        elif "categories" in user_input.lower():
            categories = []

            for product in products:
                if product["category"] not in categories:
                    categories.append(product["category"])

            ai_response = "Categories: " + ", ".join(categories)

        elif "help" in user_input.lower():
            ai_response = "You can ask about low stock, total products, categories, or how to add a product."

        elif "add product" in user_input.lower():
            ai_response = "Go to the Add Product page and fill out the form to add a new item."

        else:
            ai_response = "I could not find an answer for it, try again!"

        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": ai_response
            }
        )

        st.rerun()