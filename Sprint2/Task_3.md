# Task 3: [Feature] Implement Basic Renderers (Divider, Selectbox, TextArea)

*   **Labels:** `feature`, `mvp`, `sprint-2`, `renderer`
*   **Depends On:** Task 1, Task 2
*   **Description:** Add support for rendering `st.divider`, `st.selectbox`, and `st.text_area` based on the spec. These are needed for the target "Example Agent Spec". Ensure they handle common parameters (`key`, `label`, `options`, `help`, etc.) and integrate with state reading (Issue #2).
*   **Step-by-Step Instructions:**
    1.  **(Create `DividerRenderer`):** Create a new class `DividerRenderer(BaseRenderer)`. Implement its `render(self, item)` method to simply call `st.divider()`. Add it to the `RENDERER_MAP`.
    2.  **(Create `SelectboxRenderer`):** Create `SelectboxRenderer(BaseRenderer)`.
        *   Implement `render(self, item)`.
        *   Get parameters like `label`, `options` (list), `key`, `help` from the `item` dictionary.
        *   Get the current value from session state: `current_value = st.session_state.get(item.get('key'))`.
        *   Calculate the initial `index` for `st.selectbox` based on `current_value` and `options`. Handle cases where the value might not be in options or is None.
        *   Call `st.selectbox(label=..., options=..., key=..., help=..., index=...)`.
        *   Add it to the `RENDERER_MAP`.
    3.  **(Create `TextAreaRenderer`):** Create `TextAreaRenderer(BaseRenderer)`.
        *   Implement `render(self, item)`.
        *   Get parameters like `label`, `key`, `help` from `item`.
        *   Get the current value from session state: `current_value = st.session_state.get(item.get('key'), '')`.
        *   Call `st.text_area(label=..., value=current_value, key=..., help=...)`.
        *   Add it to the `RENDERER_MAP`.
*   **Acceptance Criteria:**
    *   `DividerRenderer`, `SelectboxRenderer`, `TextAreaRenderer` classes exist and are registered in `RENDERER_MAP`.
    *   Specs with `type: divider`, `type: selectbox`, `type: text_area` render correctly.
    *   `SelectboxRenderer` and `TextAreaRenderer` correctly display the initial value fetched from `st.session_state`.
