# Task 4: [Feature] Implement HTML Renderer

*   **Labels:** `feature`, `mvp`, `sprint-2`, `renderer`
*   **Depends On:** Task 1
*   **Description:** Add a renderer class to support rendering arbitrary HTML content using `st.components.v1.html`. This fulfills the requirement to add a custom HTML component rendering capability.
*   **Step-by-Step Instructions:**
    1.  **(Import):** Ensure `import streamlit.components.v1 as components` is present in the relevant file.
    2.  **(Create `HtmlRenderer`):** Create `HtmlRenderer(BaseRenderer)`.
    3.  **(Implement `render` Method):**
        *   Get the mandatory `html_content` from `item['html_content']`.
        *   Get optional parameters `width`, `height`, `scrolling` using `item.get(...)`.
        *   Call `components.html(html_content, width=width, height=height, scrolling=scrolling)`.
    4.  **(Register):** Add `HtmlRenderer` to the `RENDERER_MAP` with the key `"html"`.
*   **Acceptance Criteria:**
    *   `HtmlRenderer` class exists and is registered in `RENDERER_MAP`.
    *   A spec item like `{"type": "html", "html_content": "<h1>Hello</h1>"}` renders correctly.
    *   Optional `width`, `height`, `scrolling` parameters are passed if present in the spec.
