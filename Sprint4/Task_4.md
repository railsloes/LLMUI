# Issue 4.4: Implement Streamlit Login UI & Flow

## Description
Add login buttons for Google/Microsoft (e.g., in sidebar). Use st.button to trigger st.login("google") or st.login("microsoft"). Show these buttons only if st.experimental_user.is_logged_in is False.

Follow: https://docs.streamlit.io/develop/tutorials/authentication/google


## Acceptance Criteria
- Login buttons appear when logged out
- Clicking redirects to the correct IdP
- Successful login redirects back to the app

## Estimate
Medium

## Dependencies
- Issue 4.3

## Execution Steps
1. In app.py, add the authentication check and login buttons following the official Streamlit documentation approach for OAuth authentication:
```python
import streamlit as st

# --- Authentication Logic (Sprint 4, Task 4) ---
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# Check if user is logged in using Streamlit's built-in authentication
if not st.experimental_user.is_logged_in:
    # Display login UI
    st.title("Welcome to Agent UI")
    st.markdown("Please log in to continue.")
    
    st.sidebar.header("Login")
    
    # Following the official Streamlit documentation approach
    # https://docs.streamlit.io/develop/tutorials/authentication/google
    st.sidebar.button("Login with Google", on_click=lambda: st.login("google"))
    st.sidebar.button("Login with Microsoft", on_click=lambda: st.login("microsoft"))
    
    # Display message and stop if not logged in
    st.info("Please log in using one of the options in the sidebar to continue.")
    st.stop()

# ... (other imports, spec definitions, render_ui function) ...

# --- Authentication Logic ---
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

if not st.experimental_user.is_logged_in:
    st.sidebar.header("Login")
    google_login_button = st.sidebar.button("Login with Google", key="login_google_btn")
    ms_login_button = st.sidebar.button("Login with Microsoft", key="login_ms_btn")

    if google_login_button:
        try:
            st.login("google") # Key from secrets.toml
        except Exception as e:
             st.error(f"Could not initiate Google login: {e}")
    if ms_login_button:
         try:
              st.login("microsoft") # Key from secrets.toml
         except Exception as e:
              st.error(f"Could not initiate Microsoft login: {e}")

    # Display message and stop if not logged in
    st.info("Please log in using the sidebar to continue.")
    st.stop()
else:
    # User is logged in - proceed with storing info (Issue 4.5)
    # and showing logout (Issue 4.6)
    pass # Placeholder

# --- Main App Logic (only runs if logged in due to st.stop() above) ---
# ... (state init, API calls, rendering, interaction handling) ...
```

2. Run the app. Verify login buttons appear when not logged in. Click one, go through the IdP flow, and verify you are redirected back to the Streamlit app.
