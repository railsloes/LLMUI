# Task 9: [Feature] Implement DataEntryForm Renderer

*   **Labels:** `feature`, `mvp`, `sprint-2`, `renderer`, `form`
*   **Depends On:** Task 3, Task 8
*   **Description:** Implement the `DataEntryFormRenderer` class. This renderer handles the `"type": "data_entry_form"` spec. It must use `st.form` and render the specified input elements within it, reading default values from session state.
*   **Step-by-Step Instructions:**
    1.  **(Locate/Create Class):** Find/Create the `DataEntryFormRenderer` class.
    2.  **(Implement `render` Method):**
        *   Get the form `key` from `item.get('key')` with a random fallback if not provided.
        *   Get form title: `form_title = item.get('title', 'Data Entry Form')` 
        *   Get form elements: `form_elements = item.get('elements', [])`
        *   Get submit label: `submit_label = item.get('submit_label', 'Submit')`
        *   Initialize form submission state in session_state if not present
        *   Extract all input field keys from form elements for tracking
        *   Optionally create a debug expander to display form field information
        *   Display form title if provided
        *   Start the form context: `with st.form(key=form_key):`
        *   **(Render Elements Inside Form):** Inside the `with` block:
            *   Call `render_ui(form_elements)` to render all form elements
            *   Add submit button: `submitted = st.form_submit_button(submit_label)`
            *   Track submission in session state when submitted
        *   **(Handle Form Submission):** Outside the form context:
            *   Check if form was submitted: `if st.session_state.get(f"{form_key}_submitted"):`
            *   Process the form data and display success message
            *   Show the submitted values in an expander
            *   Reset the submission state to prevent re-processing
*   **Acceptance Criteria:**
    *   `DataEntryFormRenderer` class exists and renders when `"type": "data_entry_form"` is encountered.
    *   It uses `st.form` with the specified key.
    *   It renders nested elements inside the form using the existing `render_ui` function.
    *   It displays an optional form title.
    *   An `st.form_submit_button` is present inside the form.
    *   Form submission is properly handled with state management to prevent re-processing.
    *   Submitted form values are displayed to the user.
