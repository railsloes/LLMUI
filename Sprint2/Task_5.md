# Task 5: [Task] Define Static Specs & Implement Navigation Logic

*   **Labels:** `task`, `mvp`, `sprint-2`, `navigation`, `setup`
*   **Description:** Define the three static spec examples (`SPEC_V1`, `SPEC_V2`, `SPEC_V3`) in `app.py` based on the target "Example Agent Spec" and introduce variations. Update the sidebar navigation to switch between these three specs by setting `st.session_state['current_spec_version']`. Implement the logic to select the correct spec for rendering.
*   **Step-by-Step Instructions:**
    1.  **(Define Specs):** In `app.py`, create three Python variables (`SPEC_V1`, `SPEC_V2`, `SPEC_V3`) holding the spec lists (as Python lists of dictionaries).
        *   `SPEC_V1`: Use the exact "Example Agent Spec" provided previously (Markdown, Columns, Form, Chat, Divider).
        *   `SPEC_V2`: Create a variation (e.g., change the Markdown content, simplify the form fields, remove the chat).
        *   `SPEC_V3`: Create another variation that includes at least one element using `"type": "html"`.
    2.  **(Update Sidebar):** Modify the `st.sidebar.button` section:
        *   Change button labels (e.g., "Show Spec V1", "Show Spec V2", "Show Spec V3").
        *   Update the `key` for each button (e.g., `nav_v1_btn`).
        *   Inside the `if st.sidebar.button(...)` block for each, set `st.session_state['current_spec_version'] = 'V1'` (or 'V2', 'V3').
        *   Ensure `st.rerun()` is called after setting the state.
    3.  **(Initialize Default View):** Ensure `st.session_state['current_spec_version']` is initialized to `'V1'` if it doesn't exist.
    4.  **(Implement Spec Selection):** Before the `render_ui` call in the main part of the script, add logic:
        ```python
        if st.session_state['current_spec_version'] == 'V1':
            spec_to_render = SPEC_V1
        elif st.session_state['current_spec_version'] == 'V2':
            spec_to_render = SPEC_V2
        elif st.session_state['current_spec_version'] == 'V3':
            spec_to_render = SPEC_V3
        else: # Fallback
            spec_to_render = [{"type": "markdown", "content": "**Error:** Invalid spec version selected."}]
        # Now call render_ui(spec_to_render)
        ```
*   **Acceptance Criteria:**
    *   `SPEC_V1`, `SPEC_V2`, `SPEC_V3` variables exist and contain distinct spec structures. `V3` uses the `html` type.
    *   Sidebar buttons correctly update `st.session_state['current_spec_version']`.
    *   The correct spec variable is selected and passed to `render_ui` based on the session state.
    *   The UI changes (partially, based on implemented renderers) when clicking sidebar buttons.
