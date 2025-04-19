# Task 2: [Task] Adapt Input Renderers for State Reading

*   **Labels:** `task`, `mvp`, `sprint-2`, `renderer`, `state-management`
*   **Depends On:** Task 1
*   **Description:** Modify the renderers for input elements (`TextInputRenderer`, and later `SelectboxRenderer`, `TextAreaRenderer`) to correctly read their default/current value from `st.session_state` based on their `key`. Remove the problematic logic from the PoC that attempted to write back to session state directly during rendering. State *updates* will be handled separately, especially for forms (See Issue #10).
*   **Step-by-Step Instructions:**
    1.  **(Locate `TextInputRenderer`):** Open the file containing the `TextInputRenderer` class.
    2.  **(Modify `render` Method):** Inside the `render(self, item)` method:
        *   Find the line calling `st.text_input(...)`.
        *   Ensure the `value` parameter is set to read from session state using `value=st.session_state.get(item.get('key'), '')` (or another appropriate default if the key might be missing, though keys should be present for stateful elements).
        *   **Delete** the old logic that looked like `st.session_state[key] = st.text_input(...)` or used `f"{key}_input"`. The call should now be a simple `st.text_input(..., value=st.session_state.get(item.get('key'), ''), key=item.get('key'), ...)`.
    3.  **(Apply to Future Inputs):** Keep this pattern in mind when implementing `SelectboxRenderer` and `TextAreaRenderer` in Issue #3 – they must also read their initial value from `st.session_state` based on their `key`.
*   **Acceptance Criteria:**
    *   `TextInputRenderer` uses `value=st.session_state.get(...)` in its `st.text_input` call.
    *   The complex state write-back logic (`st.session_state[key] = ...` or using `f"{key}_input"`) is removed from `TextInputRenderer.render`.
    *   (Verified in Issue #3) `SelectboxRenderer` and `TextAreaRenderer` also read initial values correctly from `st.session_state`.
