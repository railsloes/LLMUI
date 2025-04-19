import streamlit as st
import streamlit.components.v1 as components
import random
from abc import ABC, abstractmethod
import requests

# --- Default State Initialization ---
# Define keys that should be initialized in session state
DEFAULT_STATES = {
    # Navigation state
    'current_view': 'text',  # Legacy view selection
    'current_spec_version': 'V1',  # Default to Spec V1
    
    # SPEC_V1 form fields
    'task_title': '',
    'task_description': '',
    'task_priority': 'Medium',
    'task_assignee': 'John',
    'agent_chat_input': '',  # Chat input for agent_chat interface
    
    # SPEC_V2 form fields
    'quick_task_name': '',
    'quick_task_priority': 'Low',
    
    # SPEC_V3 form fields
    'v3_note': '',
    
    # Data Entry Form fields
    'full_name': '',
    'email': '',
    'role': 'Developer',  # Default value for selectbox
    'bio': '',
    
    # Chat Interface state
    'support_chat_messages': [],  # List to store chat messages
    'support_chat_input': '',     # Input field for chat
    
    # Legacy form fields
    'form_first_name': '',
    'form_last_name': '',
    'form_contact_method': 'Email',
    'form_comments': '',
    'form_submit_button_clicked': False,
}

# Initialize session state keys if they don't exist
for key, default_value in DEFAULT_STATES.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

st.set_page_config(layout="wide") # Optional: Use wider layout
st.title("PoC: Streamlit Dynamic UI Core")
st.markdown("Initial application structure.")

# --- Define Service URL ---
SPEC_SERVICE_URL = "http://localhost:5001/get_spec"

# --- Function to Fetch Spec from Service ---
@st.cache_data(ttl=10) # Cache for 10 seconds to avoid spamming the service
def fetch_spec_from_service(version: str):
    """Fetches the UI specification from the local service."""
    try:
        url = f"{SPEC_SERVICE_URL}/{version}"
        response = requests.get(url, timeout=5) # Added timeout
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        spec = response.json()
        print(f"Successfully fetched spec for version {version} from {url}")
        return spec
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching spec from service at {url}: {e}")
        print(f"Error fetching spec from service at {url}: {e}")
        # Return a minimal fallback spec or an empty list
        return [
            {"type": "markdown", "text": f"## Error\n\nCould not connect to the specification service at `{url}`. Please ensure it's running.\n\n**Error details:** {e}"}
        ]
    except Exception as e:
        st.error(f"An unexpected error occurred while fetching the spec: {e}")
        print(f"An unexpected error occurred while fetching the spec: {e}")
        return [
            {"type": "markdown", "text": f"## Error\n\nAn unexpected error occurred: {e}"}
        ]

# --- Renderer Classes ---

class BaseRenderer(ABC):
    """Base class for all UI element renderers."""
    @abstractmethod
    def render(self, item: dict):
        """Renders the UI element based on the item spec.

        Args:
            item (dict): The specification dictionary for the UI element.
        """
        raise NotImplementedError

class MarkdownRenderer(BaseRenderer):
    """Renders Markdown content."""
    def render(self, item: dict):
        st.markdown(item.get("text", ""), unsafe_allow_html=False)

class TextInputRenderer(BaseRenderer):
    """Renders a text input widget, reading state from session_state."""
    def render(self, item: dict):
        """Renders a text input with value from session state.
        
        Args:
            item (dict): Spec containing 'key', 'label', and optionally 'input_type', 'help'.
        """
        key = item.get("key")
        label = item.get("label", "")
        input_type = item.get("input_type", "default")
        help_text = item.get("help")
        default_value = item.get("default", "")
        
        # Skip if no key is provided (we need a key for state management)
        if not key:
            st.warning(f"Text input '{label}' missing required 'key' property.")
            st.text_input(label=label, help=help_text, type=input_type)
            return
            
        # Ensure the key exists in session state
        if key not in st.session_state:
            st.session_state[key] = default_value
            
        # Get the current value from session state (for debug purposes only)
        current_value = st.session_state[key]
            
        # Simple approach - just use the session state key directly
        # This lets Streamlit handle the state management automatically
        value = st.text_input(
            label=label,
            key=key,  # Use the session state key directly 
            help=help_text,
            type=input_type
        )
        
        # No need to manually update session state as Streamlit does this for us
        # We'll just add a debug print to help track changes
        if value and current_value != value:
            print(f"Text input '{key}' updated to: {value}")

class ButtonRenderer(BaseRenderer):
    """Renders a button widget with proper state management."""
    def render(self, item: dict):
        """Renders a button and manages its clicked state in session_state.
        
        Args:
            item (dict): Spec containing 'label' and 'key'.
                label: Text to display on the button
                key: Unique identifier for the button
        """
        label = item.get("label", "Button")
        key = item.get("key")
        
        # Skip if no key is provided (we need a key for state management)
        if not key:
            st.warning(f"Button '{label}' missing required 'key' property.")
            st.button(label=label)  # Just render without state management
            return
            
        # Initialize button state if not present
        if f"{key}_clicked" not in st.session_state:
            st.session_state[f"{key}_clicked"] = False
            
        # Render the button and capture click
        if st.button(label=label, key=key):
            # Set clicked state to True when button is pressed
            st.session_state[f"{key}_clicked"] = True
            print(f"Button '{key}' clicked, state set to True")

class ChatMessageRenderer(BaseRenderer):
    """Renders a chat message."""
    def render(self, item: dict):
        role = item.get("role", "assistant")
        avatar = item.get("avatar")
        text = item.get("text", "")
        with st.chat_message(name=role, avatar=avatar):
            st.markdown(text)

class DividerRenderer(BaseRenderer):
    """Renders a horizontal divider."""
    def render(self, item: dict):
        """Renders a horizontal divider line.
        
        Args:
            item (dict): Spec is not used for this renderer.
        """
        st.divider()

class SelectboxRenderer(BaseRenderer):
    """Renders a dropdown selection box."""
    def render(self, item: dict):
        """Renders a selectbox with options and handles state management.
        
        Args:
            item (dict): Spec containing 'key', 'label', 'options', and optionally 'help'.
        """
        key = item.get("key")
        label = item.get("label", "")
        options = item.get("options", [])
        help_text = item.get("help")
        default_index = item.get("default_index", 0)
        
        # Skip if no key is provided (we need a key for state management)
        if not key:
            st.warning(f"Selectbox '{label}' missing required 'key' property.")
            st.selectbox(label=label, options=options, help=help_text)
            return
            
        # Skip if no options are provided
        if not options:
            st.warning(f"Selectbox '{label}' has no options.")
            return
            
        # Ensure the key exists in session state with a valid default
        if key not in st.session_state:
            default_value = options[default_index] if 0 <= default_index < len(options) else options[0]
            st.session_state[key] = default_value
        
        # Get current value from session state (for debug purposes only)
        current_value = st.session_state[key]
            
        # Simple approach - just use the session state key directly
        # This lets Streamlit handle the state management automatically
        selected_value = st.selectbox(
            label=label,
            options=options,
            key=key,  # Use the session state key directly
            help=help_text
        )
        
        # No need to manually update session state as Streamlit does this for us
        # We'll just add a debug print to help track changes
        if selected_value and current_value != selected_value:
            print(f"Selectbox '{key}' updated to: {selected_value}")

class TextAreaRenderer(BaseRenderer):
    """Renders a multi-line text input area."""
    def render(self, item: dict):
        """Renders a text area with value from session state.
        
        Args:
            item (dict): Spec containing 'key', 'label', and optionally 'height', 'help'.
                key: Unique identifier for the text area
                label: Display label for the text area
                height: Optional height in pixels (default: 100)
                help: Optional help text to display
                default: Optional default value for the text area
        
        Returns:
            None: The component renders directly to the Streamlit UI
        """
        key = item.get("key")
        label = item.get("label", "")
        height = item.get("height", 100)  # Default height: 100px
        help_text = item.get("help")
        default_value = item.get("default", "")
        
        # Skip if no key is provided (we need a key for state management)
        if not key:
            st.warning(f"Text area '{label}' missing required 'key' property.")
            st.text_area(label=label, height=height, help=help_text)
            return
            
        # Ensure the key exists in session state
        if key not in st.session_state:
            st.session_state[key] = default_value
            
        # Get the current value from session state
        current_value = st.session_state[key]

        # Simple approach - just use the session state key directly
        # This lets Streamlit handle the state management automatically
        value = st.text_area(
            label=label,
            key=key,  # Use the session state key directly
            height=height,
            help=help_text
        )
        
        # No need to manually update session state as Streamlit does this for us
        # We'll just add a debug print to help track changes
        if value and current_value != value:
            print(f"Text area '{key}' updated to: '{value[:20]}...'")

class HtmlRenderer(BaseRenderer):
    """Renders arbitrary HTML content using streamlit.components.v1.html."""
    def render(self, item: dict):
        """Renders HTML content.
        
        Args:
            item (dict): Spec containing 'html_content' and optionally 'width', 'height', 'scrolling'.
        """
        # Get the mandatory HTML content
        html_content = item.get("html_content", "")
        if not html_content:
            st.warning("HtmlRenderer: No HTML content provided.")
            return
            
        # Get optional parameters
        width = item.get("width", None)  # Default: None (auto-sizing)
        height = item.get("height", None)  # Default: None (auto-sizing)
        scrolling = item.get("scrolling", False)  # Default: False
        
        # Render the HTML content
        components.html(
            html_content,
            width=width,
            height=height,
            scrolling=scrolling
        )

# --- New Tabs Renderer ---
class TabsRenderer(BaseRenderer):
    """Renders UI elements within st.tabs."""
    def render(self, item: dict):
        """Renders multiple tabs, each with its own set of child elements.
        
        Args:
            item (dict): Spec containing 'names' (list of tab titles) and 
                         'children' (list of lists, where each inner list 
                         contains the spec for elements within the corresponding tab).
                names: List of strings for tab titles.
                children: List of lists of UI component specs. Must have the same length as 'names'.
        """
        tab_names = item.get("names", [])
        tab_children = item.get("children", [])

        if not tab_names or not tab_children or len(tab_names) != len(tab_children):
            st.error(f"Error rendering tabs: 'names' and 'children' lists must be non-empty and have the same length. Got {len(tab_names)} names and {len(tab_children)} children sets.")
            print(f"Tab rendering error: Mismatched or empty names/children. Names: {tab_names}, Children Spec Count: {len(tab_children)}")
            return

        # Create the tabs
        tabs = st.tabs(tab_names)

        # Render children within each tab
        for i, tab in enumerate(tabs):
            with tab:
                print(f"Rendering content for tab: '{tab_names[i]}' ({len(tab_children[i])} elements)")
                # Ensure children for the tab is a list before rendering
                if isinstance(tab_children[i], list):
                    render_ui(tab_children[i]) # Recursively render the spec for this tab
                else:
                    st.error(f"Invalid children specification for tab '{tab_names[i]}'. Expected a list of components.")
                    print(f"Error rendering tab '{tab_names[i]}': Children spec is not a list: {tab_children[i]}")

class ColumnsRenderer(BaseRenderer):
    """Renders content in a multi-column layout."""
    def render(self, item: dict):
        """Renders content in columns based on spec and children properties.
        
        Args:
            item (dict): Spec containing 'spec' (column widths) and 'children' (content for each column).
                spec: List of relative widths for columns (default: [1] for single column)
                children: List of lists, where each inner list contains components for a column
        """
        # Get column configuration (widths)
        column_config = item.get("spec", [1])  # Default to one column if spec missing
        
        # Get nested children specs (content for each column)
        children_specs = item.get("children", [])  # Should be a list of lists
        
        # Handle legacy 'columns' property if present (backward compatibility)
        if not children_specs and "columns" in item:
            children_specs = item.get("columns", [])
            print(f"Using legacy 'columns' property instead of 'children'")
            
        # Create Streamlit columns with specified widths
        cols = st.columns(column_config)
        
        # Validate column count matches content count
        if len(cols) != len(children_specs):
            st.error(f"Column mismatch: {len(cols)} columns defined but {len(children_specs)} content groups provided.")
            return
        
        # Render content in each column
        for i, column_content_spec in enumerate(children_specs):
            if i < len(cols):  # Safety check
                with cols[i]:
                    # Recursively render the content in this column
                    render_ui(column_content_spec)
                    
        # Print feedback for debugging
        print(f"Rendered {len(cols)} columns with {len(children_specs)} content groups")


class DataEntryFormRenderer(BaseRenderer):
    """Renders a data entry form with input fields and a submit button."""
    def render(self, item: dict):
        """Renders a form with input elements and handles form submission.
        
        Args:
            item (dict): Spec containing 'key' (form ID) and 'elements' (list of form elements).
                key: Unique identifier for the form
                elements: List of UI components to render within the form
                title: Optional title for the form
                submit_label: Text for the submit button
        """
        # Get form configuration
        form_key = item.get("key", "data_form_" + str(random.randint(1000, 9999)))
        form_title = item.get("title", "Data Entry Form")
        form_elements = item.get("elements", [])
        submit_label = item.get("submit_label", "Submit")
        
        # Initialize form submission state if not present
        if f"{form_key}_submitted" not in st.session_state:
            st.session_state[f"{form_key}_submitted"] = False

        # Extract all input field keys from the form elements for tracking
        form_field_keys = []
        for element in form_elements:
            if isinstance(element, dict) and "key" in element:
                form_field_keys.append(element.get("key"))
        
        # Create a debug expander for this form
        with st.expander(f"Debug: {form_title} Form Fields", expanded=False):
            st.write("Form field keys:", form_field_keys)
            st.write("Current values in session state:")
            form_values = {k: st.session_state.get(k, "") for k in form_field_keys}
            st.json(form_values)
        
        # Display form title if provided
        if form_title:
            st.subheader(form_title)
            
        # Create Streamlit form
        with st.form(key=form_key):
            # Render all form elements
            render_ui(form_elements)
            
            # Add submit button
            submitted = st.form_submit_button(submit_label)
            
            # Track submission in session state
            if submitted:
                st.session_state[f"{form_key}_submitted"] = True
                print(f"Form '{form_key}' submitted, state set to True")
                
                # Explicitly extract form values from form widgets and update session state
                # This is necessary because Streamlit's form values aren't immediately reflected in session_state
                for field_key in form_field_keys:
                    # The form widget key in Streamlit's internal state has a special prefix
                    internal_key = f"{form_key}-{field_key}"
                    if internal_key in st.session_state:
                        st.session_state[field_key] = st.session_state[internal_key]
                        print(f"Updated form field '{field_key}' with value: {st.session_state[field_key]}")
        
        # Handle form submission (outside the form context)
        # This follows the state management policy by checking and resetting state
        if st.session_state.get(f"{form_key}_submitted"):
            # Process the form data
            st.success(f"Form '{form_key}' submitted successfully!")
            
            # Show the submitted values
            with st.expander("Submitted Form Values", expanded=True):
                submitted_values = {k: st.session_state.get(k, "") for k in form_field_keys}
                st.json(submitted_values)
                
            print(f"Form '{form_key}' submitted with data: {st.session_state}")
            
            # Reset the submission state to prevent re-processing
            st.session_state[f"{form_key}_submitted"] = False
            print(f"Reset form submission state for '{form_key}'")


class ChatInterfaceRenderer(BaseRenderer):
    """Renders a chat interface with message history and input field."""
    def render(self, item: dict):
        """Renders a chat interface with message display and input components.
        
        Args:
            item (dict): Spec containing chat interface configuration.
                key: Unique identifier for the chat interface
                messages_key: Key to store messages in session state
                input_key: Key for the chat input field
                placeholder: Placeholder text for the input field
                send_label: Label for the send button
        """
        # Get chat configuration
        chat_key = item.get("key", "chat_interface")
        messages_key = item.get("messages_key", f"{chat_key}_messages")
        input_key = item.get("input_key", f"{chat_key}_input")
        placeholder = item.get("placeholder", "Type a message...")
        send_label = item.get("send_label", "Send")
        
        # Initialize messages in session state if not already present
        if messages_key not in st.session_state:
            st.session_state[messages_key] = []
            
        # Initialize message processing state if not present
        if f"{chat_key}_new_message" not in st.session_state:
            st.session_state[f"{chat_key}_new_message"] = False
            
        # Initialize last message content if not present
        if f"{chat_key}_last_message" not in st.session_state:
            st.session_state[f"{chat_key}_last_message"] = ""
            
        # Display chat messages
        for message in st.session_state[messages_key]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        # Chat input
        user_input = st.chat_input(placeholder=placeholder, key=input_key)
        
        # Handle new message input
        if user_input:
            # Store the message content and set the processing flag
            st.session_state[f"{chat_key}_last_message"] = user_input
            st.session_state[f"{chat_key}_new_message"] = True
            print(f"New message received in chat '{chat_key}': {user_input}")
            
        # Process new message (if flag is set)
        if st.session_state[f"{chat_key}_new_message"]:
            # Get the message content
            user_input = st.session_state[f"{chat_key}_last_message"]
            
            # Add user message to chat history
            st.session_state[messages_key].append({"role": "user", "content": user_input})
            
            # Display the new message
            with st.chat_message("user"):
                st.markdown(user_input)
                
            # Generate a response (in a real app, this would call an API or model)
            response = f"You said: {user_input}"
            
            # Add assistant response to chat history
            st.session_state[messages_key].append({"role": "assistant", "content": response})
            
            # Display the response
            with st.chat_message("assistant"):
                st.markdown(response)
                
            # Reset the new message flag to prevent reprocessing
            st.session_state[f"{chat_key}_new_message"] = False
            print(f"Processed message and reset state for chat '{chat_key}'")
                
        # Print debug info
        print(f"Chat interface '{chat_key}' rendered with {len(st.session_state.get(messages_key, []))} messages")

# --- Renderer Dispatcher Map ---

RENDERER_MAP = {
    "markdown": MarkdownRenderer,
    "text_input": TextInputRenderer,
    "text_area": TextAreaRenderer,
    "selectbox": SelectboxRenderer,
    "button": ButtonRenderer,
    "divider": DividerRenderer,
    "columns": ColumnsRenderer,
    "chat_message": ChatMessageRenderer, # Deprecated - Use ChatInterfaceRenderer
    "chat_interface": ChatInterfaceRenderer, # Combined chat input and history
    "data_entry_form": DataEntryFormRenderer,
    "html": HtmlRenderer,
    "tabs": TabsRenderer # Added Tabs Renderer
}

# --- UI Rendering Function (Dispatcher) ---

def render_ui(spec_list):
    """Renders a list of UI specifications using the class-based dispatch.

    Args:
        spec_list (list): A list of dictionaries, each specifying a UI element.
    """
    if not isinstance(spec_list, list):
        st.error("Invalid UI specification format: Expected a list.")
        return

    for item in spec_list:
        if not isinstance(item, dict):
            st.warning("Skipping invalid item in UI spec (not a dict).")
            continue

        component_type = item.get("type")
        key = item.get("key")

        RendererClass = RENDERER_MAP.get(component_type)

        if RendererClass:
            try:
                renderer = RendererClass()
                renderer.render(item)
            except Exception as e:
                st.error(f"Error rendering type '{component_type}' (key={key}): {e}")
                print(f"Error rendering type '{component_type}' (key={key}): {e}")
        elif component_type:
            st.warning(f"Unsupported component type: '{component_type}' for key '{key}'.")
            print(f"Warning: Unsupported component type: '{component_type}' for key '{key}'.")

# --- State Management and Main Rendering Logic ---

def check_button_clicks():
    """Checks for button clicks and resets their state after processing.
    
    According to the state management policy, button states must be reset after
    detection to prevent re-triggering on subsequent reruns.
    
    Returns:
        tuple: (clicked_button_key, clicked_button_value) or (None, None) if no button was clicked
    """
    # Look for button click states in session_state
    for key in list(st.session_state.keys()):
        if key.endswith('_clicked') and st.session_state[key] is True:
            # Extract the base button key (remove '_clicked' suffix)
            base_key = key[:-8]  # Remove '_clicked' suffix
            print(f"Detected button click: {base_key}")
            
            # Get any associated value if needed
            value = st.session_state.get(base_key)
            
            # Reset the button state to prevent re-triggering
            st.session_state[key] = False
            print(f"Reset button state for {key} to False")
            
            # Return the first clicked button found (process one action per rerun)
            return base_key, value
    
    # No buttons clicked
    return None, None

# Note: All state initialization is now handled at the beginning of the script
# using the DEFAULT_STATES dictionary

# Process navigation button clicks
def process_navigation():
    """Process navigation button clicks and update the current view or spec version.
    
    Following the state management policy, this function checks for button clicks,
    updates the appropriate state variables, and resets the button state to prevent
    re-triggering on subsequent reruns.
    """
    # Check for spec version navigation buttons
    if st.session_state.get("nav_v1_btn_clicked"):
        st.session_state['current_spec_version'] = 'V1'
        st.session_state["nav_v1_btn_clicked"] = False  # Reset button state
        print("Navigating to Spec V1")
        return True  # Indicate navigation occurred
        
    if st.session_state.get("nav_v2_btn_clicked"):
        st.session_state['current_spec_version'] = 'V2'
        st.session_state["nav_v2_btn_clicked"] = False  # Reset button state
        print("Navigating to Spec V2")
        return True  # Indicate navigation occurred
        
    if st.session_state.get("nav_v3_btn_clicked"):
        st.session_state['current_spec_version'] = 'V3'
        st.session_state["nav_v3_btn_clicked"] = False  # Reset button state
        print("Navigating to Spec V3")
        return True  # Indicate navigation occurred
    
    # Check for legacy view navigation buttons
    if st.session_state.get("nav_text_btn_clicked"):
        st.session_state['current_view'] = 'text'
        st.session_state["nav_text_btn_clicked"] = False  # Reset button state
        print("Navigating to Text view")
        return True  # Indicate navigation occurred
        
    if st.session_state.get("nav_form_btn_clicked"):
        st.session_state['current_view'] = 'form'
        st.session_state["nav_form_btn_clicked"] = False  # Reset button state
        print("Navigating to Form view")
        return True  # Indicate navigation occurred
        
    if st.session_state.get("nav_chat_btn_clicked"):
        st.session_state['current_view'] = 'chat'
        st.session_state["nav_chat_btn_clicked"] = False  # Reset button state
        print("Navigating to Chat view")
        return True  # Indicate navigation occurred
        
    return False  # No navigation occurred

# Check for navigation actions and rerun if needed
if process_navigation():
    st.rerun()

# Display UI based on selected spec version or legacy view
st.sidebar.title("UI Specification Selector")

# Define available spec versions
spec_versions = ('V1', 'V2', 'V3', 'V4') # Added V4

# Determine the index for the radio button default value
default_version = st.session_state.get('current_spec_version', 'V1')
try:
    default_index = spec_versions.index(default_version)
except ValueError:
    default_index = 0 # Default to the first option if the saved version is somehow invalid

selected_version = st.sidebar.radio(
    "Select Spec Version to Fetch:", 
    spec_versions, 
    key='spec_selector',
    index=default_index # Keep selection sync'd
)

# Update session state if radio button changed
if selected_version != st.session_state.get('current_spec_version'):
    st.session_state['current_spec_version'] = selected_version
    st.rerun() # Rerun immediately to fetch new spec

# Fetch the selected spec from the service
st.sidebar.markdown("--- Fetching Spec ---")
st.sidebar.info(f"Attempting to fetch spec: {st.session_state.get('current_spec_version', 'V1')}")
current_spec = fetch_spec_from_service(st.session_state.get('current_spec_version', 'V1'))

# --- Display Content Area ---
st.header(f"Dynamic UI Area (Spec: {st.session_state.get('current_spec_version', 'V1')})")

if current_spec:
    render_ui(current_spec)
else:
    st.error("No UI specification loaded. Check service connection.")

# --- Debug Area ---
st.markdown("---")
with st.expander("Debug: Session State", expanded=False):
    st.json(st.session_state.to_dict())
