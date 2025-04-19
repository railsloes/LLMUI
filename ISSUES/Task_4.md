# Task 4: Implement State Management & Initial View

**Description:** Use `st.session_state` to manage the active view. Initialize `st.session_state['current_view'] = 'text'` if it doesn't exist. Based on the value of `st.session_state['current_view']`, select the correct spec dictionary (`TEXT_SPEC`, `FORM_SPEC`, or `CHAT_SPEC`) and pass it to the `render_ui` function.

**Acceptance Criteria:** The app starts and correctly renders the `TEXT_SPEC` UI by default using the `render_ui` function and `st.session_state`.

**Estimate:** S

**Depends on:** Task 2, Task 3

**Execution Steps:**

1.  In `app.py`, below the `render_ui` function definition, add the state management and rendering logic:
    ```python
    # --- State Management and Main Rendering Logic ---
    
    # Initialize session state for the current view if it doesn't exist
    if 'current_view' not in st.session_state:
        st.session_state['current_view'] = 'text' # Default view
    
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
    
    # Add view switching buttons (Task 5 will place them properly)
    st.divider()
    st.subheader("View Navigation (Placeholder Location)")
    # (Button logic will go here in Task 5)

    # Optional: Display session state for debugging
    st.divider()
    with st.expander("Show Session State (Debug)"):
         st.json(st.session_state.to_dict())
    ```
2.  Save `app.py`.
3.  Run `streamlit run app.py`. Verify the app loads, shows "Current View: Text", and renders the markdown from `TEXT_SPEC`. Check the debug expander.
