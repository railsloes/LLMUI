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
                key = item.get("key")
                
                # Handle text input with default value from session state
                if key:
                    # Store the input value in session state when it changes
                    new_value = st.text_input(
                        label=item.get("label", ""),
                        value=st.session_state[key],
                        key=f"{key}_input",  # Use a different key for the widget
                        help=item.get("help"),
                        type=input_type
                    )
                    # Update session state with new value
                    st.session_state[key] = new_value
                else:
                    # For inputs without keys, just render them normally
                    st.text_input(
                        label=item.get("label", ""),
                        help=item.get("help"),
                        type=input_type
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

# --- State Management and Main Rendering Logic ---

# Initialize session state for the current view and form values if they don't exist
if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'text' # Default view

# Initialize form field values if they don't exist
if 'form_first_name' not in st.session_state:
    st.session_state['form_first_name'] = ''
if 'form_last_name' not in st.session_state:
    st.session_state['form_last_name'] = ''

# Determine which spec to render based on the current state
if st.session_state['current_view'] == 'text':
    spec_to_render = TEXT_SPEC
elif st.session_state['current_view'] == 'form':
    spec_to_render = FORM_SPEC
elif st.session_state['current_view'] == 'chat':
    spec_to_render = CHAT_SPEC
else:
    # Fallback or error case
    st.error(f"Unknown view state: {st.session_state['current_view']}")
    spec_to_render = [{"component": "markdown", "text": "**Error:** Invalid view state."}]

# Render the selected UI specification
st.header(f"Current View: {st.session_state['current_view'].capitalize()}")
st.divider()
render_ui(spec_to_render)

# --- View Navigation Buttons (in Sidebar) ---
st.sidebar.header("Change View")

if st.sidebar.button("Show Text", key="nav_text_btn"):
    st.session_state['current_view'] = 'text'
    # Immediately rerun to reflect change
    st.rerun()

if st.sidebar.button("Show Form", key="nav_form_btn"):
    st.session_state['current_view'] = 'form'
    st.rerun()

if st.sidebar.button("Show Chat", key="nav_chat_btn"):
    st.session_state['current_view'] = 'chat'
    st.rerun()

# Optional: Display session state for debugging
st.divider()
with st.expander("Show Session State (Debug)"):
    st.json(dict(st.session_state))
