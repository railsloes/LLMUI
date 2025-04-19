# Task 7: [Feature] Implement Columns Layout Renderer

*   **Labels:** `feature`, `mvp`, `sprint-2`, `renderer`, `layout`
*   **Depends On:** Task 1
*   **Description:** Implement the `ColumnsRenderer` class to handle the `"type": "columns"` specified in the agent spec. This is crucial for creating structured layouts and requires handling nested component rendering via recursion.
*   **Step-by-Step Instructions:**
    1.  **(Create `ColumnsRenderer`):** Define `ColumnsRenderer(BaseRenderer)`.
    2.  **(Implement `render` Method):**
        *   Get the column configuration: `column_config = item.get('spec', [1])` (default to one column if spec missing).
        *   Get the nested children specs: `children_specs = item.get('children', [])` (should be a list of lists).
        *   Call `cols = st.columns(column_config)`.
        *   **Add Validation:** Check if `len(cols) == len(children_specs)`. If not, display an error using `st.error()` and return.
        *   **(Loop & Recurse):** Iterate through `children_specs` using `enumerate`: `for i, column_content_spec in enumerate(children_specs):`.
            *   Inside the loop, use the column context manager: `with cols[i]:`.
            *   Inside the `with` block, make a recursive call to the main dispatcher function: `render_ui(column_content_spec)`. (Make sure `render_ui` is accessible, either pass it in or make the renderer classes methods of a larger App class that holds `render_ui`).
    3.  **(Register):** Add `ColumnsRenderer` to the `RENDERER_MAP` with key `"columns"`.
*   **Acceptance Criteria:**
    *   `ColumnsRenderer` class exists and is registered.
    *   Specs containing `{"type": "columns", "spec": [...], "children": [[...], [...]]}` render correctly with content placed in the specified columns.
    *   Nested components within columns are rendered correctly due to recursive calls.
    *   Handles mismatch between `spec` and `children` lengths gracefully.
