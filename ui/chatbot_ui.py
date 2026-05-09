import streamlit as st

from openai import OpenAI
from services import ai_service


def chatbot_render(api_key):
    st.header("Chatbot")
    st.caption("Ask questions about inventory, stock, categories, or product management.")
    st.divider()

    products = st.session_state["products"]

    if not api_key:
        st.error("Open AI Key was not found")
        st.stop()

    client = OpenAI(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "Hi! How can I help you?"
            }
        ]

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Ask a question...")

    if user_input:
        st.session_state["messages"].append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                context = ai_service.build_inventory_context(products)

                ai_response = ai_service.get_ai_response(
                    client,
                    st.session_state["messages"],
                    context
                )

                st.markdown(ai_response)
                logs = ai_service.load_logs("ai_logs.json")

                logs.append(
                    {
                        "user_message": user_input,
                        "ai_response": ai_response
                    }
                )

                ai_service.save_logs("ai_logs.json", logs)

        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": ai_response
            }
        )

        st.rerun()