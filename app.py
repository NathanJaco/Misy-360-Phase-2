import streamlit as st
from data.data_manager import DataManager
from ui import dashboard_ui
from ui import inventory_ui


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

users = user_manager.load_data()
products = product_manager.load_data()

st.session_state["products"] = products

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
    st.subheader("Log In")

    with st.container(border=True):
        email_input = st.text_input("Email", key="email_login")
        password_input = st.text_input("Password", type="password", key="password_login")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Log In", key="real_login_btn", type="primary", use_container_width=True):
                user_found = None
                role = None

                for user in users:
                    if user["email"] == email_input and user["password"] == password_input:
                        user_found = user
                        role = user["role"]
                        break

                if user_found:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = user_found
                    st.session_state["role"] = role

                    if role == "Owner":
                        st.session_state["page"] = "owner_dashboard"
                    else:
                        st.session_state["page"] = "employee_dashboard"

                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")

        with col2:
            if st.button("Go to Register", key="go_register_btn", use_container_width=True):
                st.session_state["page"] = "register"
                st.rerun()

elif st.session_state["page"] == "register":
    st.subheader("Register")

    with st.container(border=True):
        full_name = st.text_input("Name", key="full_name_register")
        new_email = st.text_input("Email", key="email_register")
        new_password = st.text_input("Password", type="password", key="password_register")
        new_role = st.selectbox("Role", ["Owner", "Employee"], key="role_register")

        if st.button("Create Account", key="create_account_btn", type="primary", use_container_width=True):
            email_exists = False

            for user in users:
                if user["email"] == new_email:
                    email_exists = True

            if not full_name or not new_email or not new_password:
                st.warning("Please complete all fields")

            elif email_exists:
                st.error("An account with that email already exists")

            else:
                users.append(
                    {
                        "name": full_name,
                        "email": new_email,
                        "password": new_password,
                        "role": new_role
                    }
                )

                user_manager.save_data(users)

                st.success("Account created!")
                st.session_state["page"] = "login"
                st.rerun()

elif st.session_state["page"] == "owner_dashboard":
    dashboard_ui.owner_dashboard_render()

elif st.session_state["page"] == "employee_dashboard":
    inventory_ui.employee_dashboard_render()

    
elif st.session_state["page"] == "add_product":
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

                    st.success("Product saved successfully!")
                    st.rerun()

elif st.session_state["page"] == "manage_products":
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
                        new_list = []

                        for item in products:
                            if item["name"] != product["name"]:
                                new_list.append(item)

                        products = new_list

                        product_manager.save_data(products)

                        st.success("Product deleted successfully!")
                        st.rerun()

elif st.session_state["page"] == "chatbot":
    st.header("Chatbot")
    st.caption("Ask questions about inventory, stock, categories, or product management.")
    st.divider()

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

elif st.session_state["page"] == "update_product":
    st.header("Update Product")
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
            new_price = st.number_input("New Price", min_value=0.0)
            new_stock = st.number_input("New Stock", min_value=0)

            if st.button("Update", type="primary", use_container_width=True):
                for product in products:
                    if product["name"] == selected_product:
                        product["price"] = new_price
                        product["stock"] = new_stock

                product_manager.save_data(products)

                st.success(f"{selected_product} updated successfully!")
                st.rerun()