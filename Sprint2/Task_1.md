# Task 1: [Refactor] Convert `render_ui` to Class-Based Structure

*   **Labels:** `refactor`, `mvp`, `sprint-2`, `renderer`
*   **Description:** Refactor the existing monolithic `render_ui` function in `app.py` to use a class-based approach for better maintainability and extensibility. This involves creating a base renderer class and specific renderer classes for components already handled in the PoC. The main `render_ui` function will become a dispatcher. Change the spec key from `component` to `type` for consistency.
*   **Step-by-Step Instructions:**
    1.  **(Define Base Class):** In `app.py` (or create a new `renderers.py` and import it), define a base class `BaseRenderer` with an abstract `render(self, item)` method (e.g., it can raise `NotImplementedError`).
    2.  **(Create Renderer Classes):** Create classes `MarkdownRenderer`, `TextInputRenderer`, `ButtonRenderer`, `ChatMessageRenderer` that inherit from `BaseRenderer`.
    3.  **(Implement `render` Methods):** Move the rendering logic for each component type from the old `if/elif` block into the corresponding class's `render(self, item)` method. The `item` argument is the dictionary spec for that specific component.
    4.  **(Create Dispatcher Map):** In `app.py`, create a dictionary `RENDERER_MAP` that maps the string `"type"` (e.g., `"markdown"`, `"text_input"`) to the corresponding Renderer class (e.g., `RENDERER_MAP = {"markdown": MarkdownRenderer, "text_input": TextInputRenderer, ...}`).
    5.  **(Update `render_ui` Function):** Modify the main `render_ui(spec_list)` function:
        *   It should iterate through the `spec_list`.
        *   For each `item`, get its `type` using `item.get("type")`.
        *   Look up the `type` in `RENDERER_MAP` to get the correct `RendererClass`.
        *   If found, instantiate it (`renderer = RendererClass()`) and call `renderer.render(item)`.
        *   Include error handling for unknown types.
    6.  **(Update Specs):** In the *existing* `TEXT_SPEC`, `FORM_SPEC`, `CHAT_SPEC` variables, rename the `"component"` key to `"type"` for all elements.
    7.  **(Test):** Run the app. Verify that the original PoC views (Text, Form, Chat) still render correctly using the new class-based structure and the updated spec keys.
*   **Acceptance Criteria:**
    *   `BaseRenderer` class exists.
    *   `MarkdownRenderer`, `TextInputRenderer`, `ButtonRenderer`, `ChatMessageRenderer` classes exist and correctly render their respective elements based on the `item` spec.
    *   The main `render_ui(spec_list)` function uses the `RENDERER_MAP` to dispatch rendering to the correct class.
    *   The application still renders the *original* PoC specs correctly.
    *   Specs used in testing now use the key `"type"`.
