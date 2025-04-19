# Task 1: Project Setup

**Description:** Create the project directory, set up a Python virtual environment (venv), and install Streamlit. Create the main app.py file and a requirements.txt file.

**Acceptance Criteria:** A directory exists with venv, requirements.txt listing streamlit, and a minimal runnable app.py. .gitignore is present.

**Estimate:** S

**Execution Steps:**

1.  Open your terminal or command prompt.
2.  Create the project directory: `mkdir poc_streamlit_core`
3.  Navigate into the directory: `cd poc_streamlit_core`
4.  Create a Python virtual environment: `python -m venv sltvenv`
5.  Activate the virtual environment:
    *   Linux/macOS: `source sltvenv/bin/activate`
    *   Windows (Command Prompt): `sltvenv\Scripts\activate.bat`
    *   Windows (PowerShell): `sltvenv\Scripts\Activate.ps1`
6.  Install Streamlit: `pip install streamlit`
7.  Generate the requirements file: `pip freeze > requirements.txt`
8.  Create the main application file: `touch app.py` (Linux/macOS) or create a new file named `app.py` using your editor.
9.  Add initial content to `app.py`:
    ```python
    import streamlit as st
    
    st.set_page_config(layout="wide") # Optional: Use wider layout
    st.title("PoC: Streamlit Dynamic UI Core")
    st.markdown("Initial application structure.")
    ```
10. Create a `.gitignore` file: `touch .gitignore` (Linux/macOS) or create the file.
11. Add lines to `.gitignore` to ignore the virtual environment and Streamlit secrets directory:
    ```
    sltvenv/
    .streamlit/
    __pycache__/
    *.pyc
    ```
12. Run the app to verify: `streamlit run app.py`. You should see the title and markdown text in your browser.
