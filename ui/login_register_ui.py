import streamlit as st
from data.data_manager import DataManager
from services import user_service


def login_render():
    users = st.session_state["users"]

    st.subheader("Log In")

    with st.container(border=True):
        st.markdown("### Test Accounts")
        st.markdown("Owner: owner@test.com / 123")
        st.markdown("Employee: employee@test.com / 123")

    with st.container(border=True):
        email_input = st.text_input("Email", key="email_login")
        password_input = st.text_input("Password", type="password", key="password_login")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Log In", key="real_login_btn", type="primary", use_container_width=True):
                user_found = user_service.validate_login(users, email_input, password_input)

                if user_found:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = user_found
                    st.session_state["role"] = user_found["role"]

                    if user_found["role"] == "Owner":
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


def register_render():
    users = st.session_state["users"]
    user_manager = DataManager("users.json")

    st.subheader("Register")

    with st.container(border=True):
        full_name = st.text_input("Name", key="full_name_register")
        new_email = st.text_input("Email", key="email_register")
        new_password = st.text_input("Password", type="password", key="password_register")
        new_role = st.selectbox("Role", ["Owner", "Employee"], key="role_register")

        if st.button("Create Account", key="create_account_btn", type="primary", use_container_width=True):
            email_exists = user_service.email_exists(users, new_email)

            if not full_name or not new_email or not new_password:
                st.warning("Please complete all fields")

            elif email_exists:
                st.error("An account with that email already exists")

            else:
                user_service.register_user(users, full_name, new_email, new_password, new_role)

                user_manager.save_data(users)
                st.session_state["users"] = users

                st.success("Account created!")
                st.session_state["page"] = "login"
                st.rerun()