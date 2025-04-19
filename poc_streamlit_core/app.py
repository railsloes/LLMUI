import streamlit as st

st.set_page_config(layout="wide") # Optional: Use wider layout
st.title("PoC: Streamlit Dynamic UI Core")
st.markdown("Initial application structure.")

# --- Define UI Specifications ---

TEXT_SPEC = [
    {"component": "markdown", "text": "## Text View\n\nThis view displays simple static text content."},
    {"component": "markdown", "text": "Rendered from `TEXT_SPEC`."}
]

FORM_SPEC = [
    {"component": "markdown", "text": "## Form View\n\nEnter details below. Values should persist when switching views."},
    {"component": "text_input", "label": "First Name", "key": "form_first_name"},
    {"component": "text_input", "label": "Last Name", "key": "form_last_name", "type": "default"}, # Explicitly default type
    {"component": "button", "label": "Submit (Placeholder Action)", "key": "form_submit_button"}
]

CHAT_SPEC = [
    {"component": "markdown", "text": "## Chat View\n\nDisplays a simple chat history."},
    {"component": "chat_message", "role": "user", "text": "Hello Agent!"},
    {"component": "chat_message", "role": "assistant", "text": "Hello User! How can I help?"}
]

# (Rest of the app logic will go here)
