# Issue 4.6: Implement Streamlit Logout

## Description
Add a "Logout" button (e.g., in sidebar) visible only when logged in. Clicking it should call st.logout() and clear st.session_state.user_info and st.session_state.current_ui_spec.

## Acceptance Criteria
- Logout button appears only when logged in
- Clicking logs the user out (redirects, is_logged_in becomes False)
- Clears relevant session state

## Estimate
Small

## Dependencies
- Issue 4.5

## Execution Steps
1. In app.py, inside the `else:` block (where user is logged in), add the logout button logic:
```python
# (Inside the 'else:' block where user is logged in)
st.sidebar.write(f"Welcome, {st.session_state.user_info['name']}!")

if st.sidebar.button("Logout", key="logout_btn"):
    # Clear relevant session state variables
    keys_to_clear = ["user_info", "current_ui_spec", "task_id"] # Add others as needed
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.logout() # Trigger Streamlit's internal logout and redirect

# --- Main App Logic ---
# ...
```

2. Run the app, log in. Verify the Logout button appears.
3. Click it. Verify you are logged out (login buttons reappear) and check the session state debug expander to ensure user_info and current_ui_spec are cleared.
