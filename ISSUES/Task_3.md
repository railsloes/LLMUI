# Task 3: Implement Basic render_ui Function

**Description:** Create the `render_ui(spec)` function. It should accept a spec dictionary (like those defined in Task 2). Implement logic to iterate through the spec items and render `st.markdown`, `st.text_input`, `st.button`, and `st.chat_message` based on the "component" type. Pass relevant attributes (text, label, key, role) to the Streamlit functions. Include basic handling for unknown component types (e.g., `st.warning`).

**Acceptance Criteria:** The `render_ui` function exists and can successfully render the components defined in the MVP specs when passed the corresponding dictionary.

**Estimate:** M

**Execution Steps:**

1.  In `app.py`, below the spec definitions, define the `render_ui` function:
    ```python
    # --- UI Rendering Function ---
    
    def render_ui(spec):
        """Renders Streamlit UI elements based on a list-of-dicts specification."""
        if not isinstance(spec, list):
            st.error("Invalid UI specification format: Expected a list.")
            return
    
        for item in spec:
            if not isinstance(item, dict):
                st.warning("Skipping invalid item in UI spec (not a dict).")
                continue
    
            comp_type = item.get("component")
            key = item.get("key") # Pass key to interactive elements
    
            try:
                if comp_type == "markdown":
                    st.markdown(item.get("text", ""), unsafe_allow_html=False)
                elif comp_type == "text_input":
                    # Get optional 'type' (default is 'default')
                    input_type = item.get("type", "default")
                    st.text_input(
                        label=item.get("label", ""),
                        key=key,
                        help=item.get("help"),
                        type=input_type # Pass type (e.g., 'default', 'password')
                    )
                elif comp_type == "button":
                    st.button(label=item.get("label", "Button"), key=key)
                elif comp_type == "chat_message":
                    role = item.get("role", "assistant")
                    avatar = item.get("avatar")
                    with st.chat_message(name=role, avatar=avatar):
                        st.markdown(item.get("text", ""))
                # Add elif for other components like title, selectbox, metric, columns later if needed
                elif comp_type: # Only warn if component type was specified but not matched
                    st.warning(f"Unsupported component type: '{comp_type}' for key '{key}'.")
    
            except Exception as e:
                st.error(f"Error rendering component (key={key}, type={comp_type}): {e}")
    
    # (Rest of the app logic will go here)
    ```
2.  Save the `app.py` file.
