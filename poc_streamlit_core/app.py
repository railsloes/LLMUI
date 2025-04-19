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

# --- UI Rendering Function ---

def render_ui(spec):
    """Renders Streamlit UI elements based on a list-of-dicts specification."""
    if not isinstance(spec, list):
        st.error("Invalid UI specification format: Expected a list.")
        return

    for item in spec:
        if not isinstance(item, dict):
            st.warning("Skipping invalid item in UI spec (not a dict).")
            continue

        comp_type = item.get("component")
        key = item.get("key") # Pass key to interactive elements

        try:
            if comp_type == "markdown":
                st.markdown(item.get("text", ""), unsafe_allow_html=False)
            elif comp_type == "text_input":
                # Get optional 'type' (default is 'default')
                input_type = item.get("type", "default")
                st.text_input(
                    label=item.get("label", ""),
                    key=key,
                    help=item.get("help"),
                    type=input_type # Pass type (e.g., 'default', 'password')
                )
            elif comp_type == "button":
                st.button(label=item.get("label", "Button"), key=key)
            elif comp_type == "chat_message":
                role = item.get("role", "assistant")
                avatar = item.get("avatar")
                with st.chat_message(name=role, avatar=avatar):
                    st.markdown(item.get("text", ""))
            # Add elif for other components like title, selectbox, metric, columns later if needed
            elif comp_type: # Only warn if component type was specified but not matched
                st.warning(f"Unsupported component type: '{comp_type}' for key '{key}'.")

        except Exception as e:
            st.error(f"Error rendering component (key={key}, type={comp_type}): {e}")

# (Rest of the app logic will go here)
