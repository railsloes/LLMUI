# Task 6: Test Form State Persistence

**Description:** Run the application. Navigate to the "Form View". Enter distinct values into the text input fields. Navigate away to the "Text View" or "Chat View" using the buttons. Navigate back to the "Form View". Verify that the values previously entered into the text input fields are still present.

**Acceptance Criteria:** Input values within the Form View persist correctly when switching between views, demonstrating `st.session_state` working with widget keys.

**Estimate:** S

**Depends on:** Task 5

**Execution Steps:**

1.  Ensure the app is running (`streamlit run app.py`).
2.  Click the "Show Form" button in the sidebar.
3.  In the "First Name" input field, type "TestFirstName".
4.  In the "Last Name" input field, type "TestLastName".
5.  Click the "Show Text" button in the sidebar. Observe the text view.
6.  Click the "Show Form" button again.
7.  Verify: The "First Name" field should still contain "TestFirstName", and the "Last Name" field should still contain "TestLastName". This works because the `render_ui` function consistently assigns the same key ("form_first_name", "form_last_name") to these inputs, and Streamlit automatically stores widget values in `st.session_state` using their keys.
