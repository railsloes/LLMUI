# Issue 4.5: Implement Authenticated State Handling & User Info Display

## Description
After login, use st.experimental_user.is_logged_in. If True, display a welcome message (e.g., Welcome, {st.experimental_user.email}). Store the user identifier (e.g., email) in st.session_state.user_info for use in API calls. Hide login buttons.

## Acceptance Criteria
- App correctly detects logged-in state
- User email/name displayed
- st.session_state.user_info populated
- Login buttons hidden

## Estimate
Medium

## Dependencies
- Issue 4.4

## Execution Steps
1. In app.py, replace the pass # Placeholder under the else: block (where user is logged in) from Issue 4.4:
```python
# (Inside the main script flow, after the initial login check)
else: # User IS logged in
    # Store user info the first time we detect login in this session
    if st.session_state.user_info is None:
        user_email = st.experimental_user.email
        user_name = getattr(st.experimental_user, 'name', user_email) # Use email if name not available
        st.session_state.user_info = {"email": user_email, "name": user_name}
        st.success(f"Logged in as {user_name} ({user_email})") # Feedback
        # Potentially trigger initial API call here now that user is known
        # initial_spec = call_agent_simulator(...) # Needs user_id now
        # st.session_state.current_ui_spec = initial_spec.get("view_config") if initial_spec else None

    # Display welcome message in sidebar
    st.sidebar.write(f"Welcome, {st.session_state.user_info['name']}!")
    # Logout button logic will go here (Issue 4.6)

# --- Main App Logic ---
# Ensure user_info is checked before making API calls needing user_id
if st.session_state.user_info:
    # ... (API calls, rendering, interaction handling) ...
    pass
else:
     # Should not happen if st.stop() worked, but good practice
     st.error("Error: User information not available.")
```

2. Run the app, log in. Verify the welcome message appears, login buttons are gone, and the debug expander shows user_info populated in session state.
