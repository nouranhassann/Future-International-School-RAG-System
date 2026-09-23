import streamlit as st
from api_client import APIClient

st.set_page_config(page_title="School Knowledge Assistant", page_icon="🏫")

# Initialize session state
if 'api_client' not in st.session_state:
    st.session_state.api_client = APIClient()
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def do_login():
    email = st.session_state.email_input
    password = st.session_state.password_input
    success, error = st.session_state.api_client.login(email, password)
    if success:
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
    else:
        st.error(error)

def do_logout():
    st.session_state.api_client = APIClient()
    st.session_state.logged_in = False
    st.session_state.chat_history = []

# Header
st.title("🏫 Future Scholars International School")
st.subheader("Role-Based Knowledge Assistant")

if not st.session_state.logged_in:
    st.write("Please log in to access the school knowledge base.")
    
    with st.form("login_form"):
        st.text_input("Email", key="email_input")
        st.text_input("Password", type="password", key="password_input")
        st.form_submit_button("Login", on_click=do_login)
        
    st.info("Demo accounts:\n- student@example.com / password123\n- teacher@example.com / password123")

else:
    # Sidebar
    st.sidebar.title("User Profile")
    st.sidebar.write(f"**Logged in as:** {st.session_state.api_client.role.capitalize()}")
    st.sidebar.button("Logout", on_click=do_logout)
    
    # Chat Interface
    st.write("Ask questions about school policies, curriculum, and more!")
    
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])
            if "sources" in chat and chat["sources"]:
                with st.expander("Sources"):
                    for source in chat["sources"]:
                        st.write(f"- {source}")
    
    # User Input
    question = st.chat_input("Enter your question here...")
    
    if question:
        # Add to history
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
            
        with st.chat_message("assistant"):
            with st.spinner("Searching and generating answer..."):
                success, answer, sources = st.session_state.api_client.query(question)
                
                if success:
                    st.markdown(answer)
                    if sources:
                        with st.expander("Sources"):
                            for source in sources:
                                st.write(f"- {source}")
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources
                    })
                else:
                    st.error(answer)
