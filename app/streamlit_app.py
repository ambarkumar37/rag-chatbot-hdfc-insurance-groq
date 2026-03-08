import streamlit as st
import requests

# FastAPI backend URL
API_URL = "https://rag-chatbot-hdfc-insurance-groq.onrender.com"
#API_URL = "http://127.0.0.1:8086/chatendpoint"



st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")

# Show title and description.
# st.title("💬 Chatbot")
# st.write(
#     "This is a simple chatbot to generate responses. "
#     )

st.title("🛡️ HDFC ERGO Insurance Policy Assistant")

st.markdown(
"""
This AI assistant helps you understand **HDFC ERGO insurance policies**.

You can ask questions about:
- Policy coverage
- Claims process
- Exclusions
- Benefits and limits
- Policy terms

The assistant retrieves answers directly from the uploaded **policy documents** and shows the **source references** used to generate the response.
"""
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response with spinner
    with st.chat_message("assistant"):
        with st.spinner("loading..."):
            try:
                response = requests.post(
                    API_URL,
                    #json={"user_input": user_input},
                    json={"question": user_input},
                    timeout=120
                )

                if response.status_code == 200:
                    #bot_reply = response.json()["response"]
                    #bot_reply = response.json()["answer"]
                    data = response.json()
                    bot_reply = data["answer"]
                    sources = data.get("sources", [])
                else:
                    bot_reply = f"Error: {response.text}"
                    sources = []

            except requests.exceptions.RequestException as e:
                bot_reply = f"Connection error: {str(e)}"

            st.markdown(bot_reply)
            # Show sources
            if sources:
                st.markdown("### 📄 Sources used")
                
                for i, src in enumerate(sources, 1):
                    source_file = src["source"]
                    pages = src.get("pages", "")
                    
                    if pages:
                        st.markdown(f"{i}. **{source_file}** (p.{pages})")
                    else:
                        st.markdown(f"{i}. **{source_file}**")

    # Save assistant message to history
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
