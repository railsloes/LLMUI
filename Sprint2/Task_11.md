# Task 11: [Feature] Implement ChatInterface Renderer

*   **Labels:** `feature`, `mvp`, `sprint-2`, `renderer`, `chat`
*   **Depends On:** Task 8
*   **Description:** Implement the `ChatInterfaceRenderer` class to handle the `"type": "chat_interface"` spec. It should render the chat history and provide the chat input box.
*   **Step-by-Step Instructions:**
    1.  **(Locate/Create Class):** Find/Create the `ChatInterfaceRenderer` class.
    2.  **(Implement `render` Method):**
        *   Get the chat `history` list from `item.get('history', [])`.
        *   Get the component `key` from `item.get('key')`.
        *   **(Render History):** Loop through the `history` list. For each `message` dictionary:
            *   Get `role = message.get('role', 'assistant')`.
            *   Get `content = message.get('content', '')`.
            *   Use the context manager: `with st.chat_message(name=role):`.
            *   Inside the `with` block, render the content: `st.markdown(content)`.
        *   **(Render Input):** After the history loop, add the input box: `st.chat_input("Send a message...", key=f"{key}_input")`. (We need a distinct key for the input widget itself. We also previously added `task_chat_input` to DEFAULT\_STATES in Issue #6, assuming the chat input key would follow this pattern). *Note: Handling the submission of this input is deferred.*
*   **Acceptance Criteria:**
    *   `ChatInterfaceRenderer` class exists and renders when `"type": "chat_interface"` is encountered.
    *   It correctly iterates through the `history` spec and displays messages using `st.chat_message` and `st.markdown`.
    *   An `st.chat_input` widget is displayed below the chat history with the correct key.
