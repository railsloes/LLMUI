# Task 5: Implement View Switching Buttons & Logic

**Description:** Add three persistent `st.button` widgets (e.g., in the sidebar or using `st.columns` at the top/bottom): "Show Text", "Show Form", "Show Chat". Implement the logic so that clicking each button updates `st.session_state['current_view']` to 'text', 'form', or 'chat' respectively.

**Acceptance Criteria:** The three buttons are always visible. Clicking a button updates the main view to display the UI corresponding to that button's spec via the `render_ui` function on the next rerun.

**Estimate:** M

**Depends on:** Task 4

**Execution Steps:**

1.  In `app.py`, modify the placeholder section for navigation buttons. Using the sidebar is often cleanest:
    ```python
    # --- View Navigation Buttons (in Sidebar) ---
    st.sidebar.header("Change View")
    
    if st.sidebar.button("Show Text", key="nav_text_btn"):
        st.session_state['current_view'] = 'text'
        # Optional: Immediately rerun to reflect change if needed,
        # though Streamlit usually handles rerun on button click.
        # st.rerun()
    
    if st.sidebar.button("Show Form", key="nav_form_btn"):
        st.session_state['current_view'] = 'form'
        # st.rerun()
    
    if st.sidebar.button("Show Chat", key="nav_chat_btn"):
        st.session_state['current_view'] = 'chat'
        # st.rerun()
    
    # Remove the placeholder section from the main area if you added it before.
    ```
2.  Save `app.py`.
3.  Run `streamlit run app.py`.
4.  Verify the three buttons appear in the sidebar.
5.  Click each button and confirm that the main view area updates to show the corresponding content ("Text View", "Form View", "Chat View") and the "Current View" header changes. Check the session state debug area to see `current_view` update.
