import streamlit as st
import streamlit.components.v1 as components
import random
from abc import ABC, abstractmethod
import requests
import json
import os
import logging
import toml
import time
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("streamlit_app")

# --- Page Config (Must be first Streamlit command) ---
st.set_page_config(layout="wide", page_title="Agent UI") # Optional: Use wider layout

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

# --- Add Task ID Handling --- Start
if 'task_id' not in st.session_state:
    query_params = st.query_params
    task_id = query_params.get("task_id")
    if task_id:
        st.session_state.task_id = task_id
        st.info(f"Task ID received: {st.session_state.task_id}") # Optional: display confirmation
    else:
        st.session_state.task_id = None # Explicitly set to None if not found
# --- Add Task ID Handling --- End

# --- Authentication Logic (Sprint 4, Task 4) ---
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

# Debug auth configuration in secrets.toml
try:
    secrets_file = Path("/Users/federicolopez/LLMUI/LLMUI/poc_streamlit_core/.streamlit/secrets.toml")
    if secrets_file.exists():
        logger.info("Found secrets.toml file")
        secrets_content = toml.loads(secrets_file.read_text())
        
        # Check auth config structure
        if 'auth' in secrets_content:
            logger.info("Found 'auth' section in secrets.toml")
            
            if 'providers' in secrets_content['auth']:
                logger.info("Found 'providers' section in auth config")
                
                if 'google' in secrets_content['auth']['providers']:
                    google_config = secrets_content['auth']['providers']['google']
                    logger.info(f"Google provider config keys: {list(google_config.keys())}")
                    
                    # Check required fields
                    required_fields = ['client_id', 'client_secret']
                    missing_fields = [field for field in required_fields if field not in google_config]
                    
                    if missing_fields:
                        logger.error(f"Missing required fields for Google provider: {missing_fields}")
                    else:
                        logger.info("All required fields for Google provider are present")
                else:
                    logger.error("Google provider missing from auth.providers")
            else:
                logger.error("'providers' section missing from auth config")
        else:
            logger.error("'auth' section missing from secrets.toml")
    else:
        logger.error("secrets.toml file not found")
        
    # Log streamlit config directory
    logger.info(f"Streamlit config directory detected: {os.path.expanduser('~/.streamlit')}")
    try:
        from streamlit.runtime.secrets import get_secrets_dict
        app_secrets = get_secrets_dict()
        logger.info(f"App secrets keys: {list(app_secrets.keys())}")
        if 'auth' in app_secrets:
            logger.info(f"Auth config from app_secrets: {list(app_secrets['auth'].keys())}")
    except Exception as e:
        logger.error(f"Error accessing app secrets: {e}")
        
except Exception as e:
    logger.error(f"Error checking secrets.toml: {e}")

# Log the contents of st.secrets for debugging
try:
    logger.info(f"Contents of st.secrets: {st.secrets.to_dict()}")
except Exception as secret_log_e:
    logger.error(f"Could not log st.secrets: {secret_log_e}")

# --- Authentication and User State Handling (Sprint 4, Task 5) ---
if st.experimental_user.is_logged_in:
    # User is logged in - extract and store user info
    user_info = {
        "email": getattr(st.experimental_user, "email", None),
        "name": getattr(st.experimental_user, "name", None),
        "id": getattr(st.experimental_user, "id", None)
    }
    
    # Store in session state for use throughout the app
    st.session_state.user_info = user_info
    
    # Determine display name (prefer email, fallback to name)
    display_name = user_info["email"] or user_info["name"] or "User"
    
    # Display welcome message and user info
    st.title(f"Welcome, {display_name}!")
    st.sidebar.header("Account")
    st.sidebar.write(f"Signed in as: {display_name}")
    
    # Logout button implementation (Sprint 4, Task 6)
    if st.sidebar.button("Logout", key="logout_btn"):
        # Clear relevant session state variables
        keys_to_clear = ["user_info", "current_ui_spec", "task_id"] # Add others as needed
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        # Use Streamlit's built-in logout function
        st.logout()
        
else:
    # User is not logged in - show login UI
    st.title("Welcome to Agent UI")
    st.sidebar.header("Login")
    
    # Google login button
    if st.sidebar.button("Login with Google"):
        try:
            logger.info("Attempting to login with Google provider")
            st.login("google")
        except Exception as e:
            error_msg = f"Could not initiate Google login: {e}"
            logger.error(error_msg)
            st.error(error_msg)
    
    # Microsoft login button (commented out until credentials are set up)
    # if st.sidebar.button("Login with Microsoft"):
    #     try:
    #         logger.info("Attempting to login with Microsoft provider")
    #         st.login("microsoft")
    #     except Exception as e:
    #         error_msg = f"Could not initiate Microsoft login: {e}"
    #         logger.error(error_msg)
    #         st.error(error_msg)
    
    # Display message and stop if not logged in
    st.info("Please log in using one of the options in the sidebar to continue.")
    st.stop()

# --- Main App Logic (only runs if logged in due to st.stop() above) ---
st.title("PoC: Streamlit Dynamic UI Core")
st.markdown("Initial application structure.")

# --- Define Agent Simulator URLs ---
SIMULATOR_BASE_URL = "http://localhost:5001"
REMOTE_AGENT_URL = f"{SIMULATOR_BASE_URL}/get_spec"
# Note: This connects to the agent_simulator.py Flask app

# --- API Interaction ---
def fetch_spec(agent_url, version):
    """Fetches the UI specification from the remote agent service.
    
    Args:
        agent_url (str): Base URL for the agent simulator API
        version (str): Version of the UI spec to fetch (e.g., 'V1', 'V2')
        
    Returns:
        list: The UI specification as a list of components, or a fallback error UI
    """
    # Add task_id to the request if available
    params = {}
    if st.session_state.get("task_id"):
        params["task_id"] = st.session_state.get("task_id")
    
    # SPRINT 5: Add user_id (email) to the request if available
    if st.session_state.get("user_info") and st.session_state.user_info.get("email"):
        params["user_id"] = st.session_state.user_info.get("email")
    
    # Construct the URL
    url = f"{agent_url}/{version}" if version else agent_url
    
    # Append parameters to URL
    if params:
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        url += f"?{query_string}"
        logger.info(f"Fetching spec from {url} with params: {params}") 
    else:
        logger.info(f"Fetching spec from {url} (no params)")

    # Use a spinner to indicate loading
    with st.spinner(f"Loading UI specification (version {version})..."):
        # Implement retry logic
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt+1}/{max_retries} to fetch spec from {url}")
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                spec = response.json()
                
                # Log success
                logger.info(f"Successfully fetched spec for version {version} from {url}")
                logger.debug(f"Received spec: {spec}")
                
                # Reset any error-related session state
                if 'api_error' in st.session_state:
                    del st.session_state['api_error']
                    
                return spec
                
            except requests.exceptions.Timeout:
                error_msg = "Connection timed out while reaching the agent simulator."
                logger.warning(f"Timeout error on attempt {attempt+1}: {error_msg}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    
            except requests.exceptions.ConnectionError:
                error_msg = "Could not connect to the agent simulator. Is it running?"
                logger.warning(f"Connection error on attempt {attempt+1}: {error_msg}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Error communicating with the agent simulator: {str(e)}"
                logger.error(f"Request error on attempt {attempt+1}: {error_msg}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    
            except json.JSONDecodeError:
                error_msg = "Received invalid response from the agent simulator."
                logger.error(f"JSON decode error on attempt {attempt+1}: {error_msg}")
                break  # Don't retry JSON errors as they're likely not transient
                
            except Exception as e:
                error_msg = f"An unexpected error occurred: {str(e)}"
                logger.error(f"Unexpected error on attempt {attempt+1}: {error_msg}")
                break  # Don't retry unexpected errors
        
        # If we've exhausted retries or hit a non-retryable error
        # Store error in session state for reference
        st.session_state['api_error'] = error_msg
        
        # Show user-friendly error message
        st.error(error_msg)
        
        # Return a fallback UI with helpful error information
        return [
            {"type": "markdown", "text": "## Connection Error"},
            {"type": "markdown", "text": f"**{error_msg}**"},
            {"type": "markdown", "text": "### Troubleshooting Steps:"},
            {"type": "markdown", "text": "1. Ensure the agent simulator is running on port 5001\n2. Check network connectivity\n3. Try refreshing the page\n4. Contact support if the issue persists"}
        ]

# --- Agent Simulator API Call (Sprint 3, Task 6) ---
def call_agent_simulator(action_key, data_payload, task_id, user_id=None):
    """Sends interaction data to the simulator and returns the new UI spec.
    
    Args:
        action_key (str): The key of the action that was triggered
        data_payload (dict): The collected data from the UI
        task_id (str): The task ID from the session state
        user_id (str, optional): The user ID from the authenticated user
        
    Returns:
        dict or None: The parsed JSON response from the simulator, or None on error
    """
    url = f"{SIMULATOR_BASE_URL}/interact"
    
    # Prepare the payload
    payload = {
        "action_key": action_key,
        "data": data_payload,
        "task_id": task_id,
        "user_id": user_id if user_id else "anonymous_poc_user"  # Use authenticated user ID if available
    }
    headers = {"Content-Type": "application/json"}
    
    # Store the interaction details in session state for debugging/recovery
    st.session_state['last_interaction'] = {
        'timestamp': time.time(),
        'action_key': action_key,
        'data_payload': data_payload,
        'task_id': task_id,
        'user_id': user_id
    }
    
    # Log the interaction attempt
    logger.info(f"Sending interaction to agent simulator: action_key={action_key}, task_id={task_id}, user_id={user_id}")
    logger.debug(f"Full payload: {json.dumps(payload)}")
    logger.info(f"Target URL: {url}")

    # Use a spinner to indicate loading
    with st.spinner(f"Processing {action_key} action..."):
        # Implement retry logic
        max_retries = 2  # Fewer retries for interactive calls
        retry_delay = 0.5  # seconds
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt+1}/{max_retries} to send interaction to {url}")
                
                response = requests.post(url, headers=headers, json=payload, timeout=10)
                response.raise_for_status()  # Check for HTTP errors
                
                new_ui_spec_response = response.json()  # Expecting JSON like {"status": "success", "view_config": [...]}
                
                # Log success
                logger.info(f"Successfully received response from simulator for action {action_key}")
                logger.debug(f"Response: {json.dumps(new_ui_spec_response)}")
                
                # Store successful response in session state
                st.session_state['last_successful_interaction'] = {
                    'timestamp': time.time(),
                    'action_key': action_key,
                    'response': new_ui_spec_response
                }
                
                # Clear any error state
                if 'interaction_error' in st.session_state:
                    del st.session_state['interaction_error']
                    
                return new_ui_spec_response
                
            except requests.exceptions.Timeout:
                error_msg = "The request to the agent simulator timed out."
                logger.warning(f"Timeout error on attempt {attempt+1}: {error_msg}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    
            except requests.exceptions.ConnectionError:
                error_msg = "Could not connect to the agent simulator. Please ensure it's running."
                logger.warning(f"Connection error on attempt {attempt+1}: {error_msg}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Error communicating with the agent simulator: {str(e)}"
                logger.error(f"Request error on attempt {attempt+1}: {error_msg}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    
            except json.JSONDecodeError:
                error_msg = "Received invalid response format from the agent simulator."
                logger.error(f"JSON decode error on attempt {attempt+1}: {error_msg}")
                break  # Don't retry JSON errors
                
            except Exception as e:
                error_msg = f"An unexpected error occurred: {str(e)}"
                logger.error(f"Unexpected error on attempt {attempt+1}: {error_msg}")
                break  # Don't retry unexpected errors
        
        # If we've exhausted retries or hit a non-retryable error
        # Store error in session state
        st.session_state['interaction_error'] = {
            'timestamp': time.time(),
            'action_key': action_key,
            'error': error_msg
        }
        
        # Show user-friendly error message
        st.error(f"Action could not be processed: {error_msg}")
        
        # Provide a fallback response that indicates the error
        return {
            "status": "error",
            "message": error_msg,
            "view_config": [
                {"type": "markdown", "text": "## Action Processing Error"},
                {"type": "markdown", "text": f"**{error_msg}**"},
                {"type": "markdown", "text": "Your action could not be processed. Please try again or refresh the page."}
            ]
        }

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
            
            # Add debug messages for interaction detection (Sprint 3, Task 3)
            st.write(f"DEBUG: Detected form submission for form: {form_key}")  # Debug
            st.write(f"DEBUG: Action '{form_key}_form_submit' triggered. Proceeding...")  # Debug
                
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

        # Debug output for each component
        print(f"DEBUG - Rendering component: type={component_type}, key={key}")

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
# SPRINT 5: Added V6 for email-based access control demo
version_options = ["V1", "V2", "V3", "V4", "V5", "V6"]

# Add a note about V6 for email-based access control
if st.session_state.get('user_info'):
    st.sidebar.info("**V6** demonstrates email-based access control. Try logging in with:\n- feloes@gmail.com (Admin)\n- fede@urobora.com (Regular User)")

# Determine the index for the radio button default value
default_version = st.session_state.get('current_spec_version', 'V1')
try:
    default_index = version_options.index(default_version)
except ValueError:
    default_index = 0  # Default to the first option if the saved version is invalid

selected_version = st.sidebar.radio(
    "Select Spec Version to Fetch:", 
    version_options, 
    key='spec_selector',
    index=default_index  # Keep selection sync'd
)

# Update session state if version changed
if selected_version != st.session_state.get('current_spec_version'):
    st.session_state['current_spec_version'] = selected_version
    st.rerun()  # Force a rerun to fetch the new spec

# Fetch the selected spec from the remote agent
st.sidebar.markdown("--- Fetching Spec from Remote Agent ---")
st.sidebar.info(f"Attempting to fetch spec: {st.session_state.get('current_spec_version', 'V1')}")
current_spec = fetch_spec(REMOTE_AGENT_URL, st.session_state.get('current_spec_version', 'V1'))

# --- Display Content Area ---
st.header(f"Dynamic UI Area (Spec: {st.session_state.get('current_spec_version', 'V1')})") 

if current_spec:
    # Store the current spec in session state for interaction detection
    st.session_state['current_ui_spec'] = current_spec
    render_ui(current_spec)
else:
    st.error("No UI specification loaded. Check service connection.")

# --- Interaction Detection (Sprint 3, Task 3) ---
triggered_action_key = None
spec_rendered = st.session_state.get('current_ui_spec')  # Get the spec that was just rendered

# First, check for form submissions
if spec_rendered and isinstance(spec_rendered, list):
    for item in spec_rendered:
        if not isinstance(item, dict): 
            continue

        comp_type = item.get("type")
        key = item.get("key")

        if not key: 
            continue  # Skip elements without keys

        # Check for form submissions
        if comp_type == "data_entry_form":
            form_submit_key = f"{key}_submitted"
            if st.session_state.get(form_submit_key):  # Check if form was submitted
                triggered_action_key = f"{key}_form_submit"
                st.write(f"DEBUG: Detected form submission for form: {key}")  # Debug
                # Note: We don't break here because the DataEntryFormRenderer already resets the state

        # Check for button clicks
        elif comp_type == "button":
            click_state_key = f"{key}_clicked"
            if st.session_state.get(click_state_key):  # Check if button click state is True
                triggered_action_key = key
                st.write(f"DEBUG: Detected button click for key: {key}")  # Debug
                
                # Reset button state immediately (Sprint 3, Task 4)
                st.session_state[click_state_key] = False
                print(f"Reset button state for '{click_state_key}' to False")
                
                break  # Process only the first detected action

        # Add more elif checks for other interactive types if needed

# --- Action Processing and Data Collection (Sprint 3, Task 5) ---
if triggered_action_key:
    st.write(f"DEBUG: Action '{triggered_action_key}' triggered. Collecting data...")
    data_payload = {}
    spec_rendered = st.session_state.get('current_ui_spec')

    # Define which input types to collect data from
    INPUT_COMPONENT_TYPES = ["text_input", "selectbox", "text_area"] # Extend as needed

    if spec_rendered and isinstance(spec_rendered, list):
        for item in spec_rendered:
             if not isinstance(item, dict): continue
             comp_type = item.get("type")
             key = item.get("key")

             if key and comp_type in INPUT_COMPONENT_TYPES:
                 if key in st.session_state:
                     data_payload[key] = st.session_state[key]
                 else:
                     # Input might not have been rendered or state lost
                     data_payload[key] = None # Or log warning
                     st.warning(f"Could not find key '{key}' in session state during data collection.")

    st.write(f"DEBUG: Data collected: {data_payload}")
    
    # Call the Agent Simulator with the collected data (Sprint 3, Task 6)
    st.write(f"DEBUG: Calling simulator for action '{triggered_action_key}'")
    # Add user_id to the call if available
    user_id = None
    if st.session_state.get('user_info'):
        user_id = st.session_state.user_info.get('email')
    api_response = call_agent_simulator(triggered_action_key, data_payload, st.session_state.get("task_id"), user_id)

    if api_response and api_response.get("status") == "success":
         new_spec = api_response.get("view_config")
         st.session_state.current_ui_spec = new_spec
         st.write(f"DEBUG: Received new UI spec from simulator. Will update on next rerun.")
         # Optional: st.rerun() if immediate refresh needed
    elif api_response: # Handle structured errors if simulator sends them
         st.error(f"Agent Simulator Error: {api_response.get('message', 'Unknown error')}")

# --- Debug Area ---
st.markdown("---")
with st.expander("Debug: Session State", expanded=False):
    st.json(st.session_state.to_dict())
