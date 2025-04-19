# Task 8: [Task] Implement Custom Type Dispatch in Renderer

*   **Labels:** `task`, `mvp`, `sprint-2`, `renderer`
*   **Depends On:** Task 1
*   **Description:** Modify the main `render_ui` dispatcher logic/map to recognize the custom types `"data_entry_form"` and `"chat_interface"` from the spec. It should delegate the rendering of these types to their specific Renderer classes (to be created in Issues #9 and #11).
*   **Step-by-Step Instructions:**
    1.  **(Locate Dispatcher):** Find the `RENDERER_MAP` dictionary and the main `render_ui` function.
    2.  **(Add Placeholders/Classes):** Define placeholder or actual classes `DataEntryFormRenderer(BaseRenderer)` and `ChatInterfaceRenderer(BaseRenderer)` (even if empty initially).
    3.  **(Update Map):** Add entries to `RENDERER_MAP`:
        ```python
        RENDERER_MAP = {
            # ... existing entries ...
            "data_entry_form": DataEntryFormRenderer,
            "chat_interface": ChatInterfaceRenderer,
        }
        ```
    4.  **(Verify Dispatch):** Ensure the `render_ui` function's logic correctly looks up these new types and would call their (currently basic) `render` methods without errors.
*   **Acceptance Criteria:**
    *   The `render_ui` dispatcher `RENDERER_MAP` includes keys `"data_entry_form"` and `"chat_interface"` mapped to their respective (potentially placeholder) Renderer classes.
    *   When `render_ui` encounters these types in a spec, it attempts to call the correct renderer class without crashing.
