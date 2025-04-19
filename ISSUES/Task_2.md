# Task 2: Define Predefined UI Specs

**Description:** Within `app.py`, define three Python dictionary variables: `TEXT_SPEC`, `FORM_SPEC`, `CHAT_SPEC`.
*   `TEXT_SPEC`: Should contain at least one `{"component": "markdown", "text": "This is the text view."}`.
*   `FORM_SPEC`: Should contain at least two `{"component": "text_input", "label": "...", "key": "unique_form_key_1"}` elements and potentially a placeholder `{"component": "button", "label": "Submit (Placeholder)", "key": "form_submit_btn"}`. Ensure input keys are unique.
*   `CHAT_SPEC`: Should contain at least two `{"component": "chat_message", "role": "...", "text": "..."}` elements (e.g., one user, one assistant).

**Acceptance Criteria:** Three variables exist in `app.py` containing valid dictionary structures representing the UI specs for the three views, including keys for form inputs.

**Estimate:** S

**Execution Steps:**

1.  Open `app.py` in your code editor.
2.  Below the initial imports and title, define the Python dictionaries:
    ```python
    import streamlit as st
    
    st.set_page_config(layout="wide")
    st.title("PoC: Streamlit Dynamic UI Core")
    
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
    ```
3.  Save the `app.py` file.
