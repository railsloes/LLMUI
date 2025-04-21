# Sprint 6 - Task 6.4: Deployment Preparation

**Description:**
Prepare the application for deployment. This involves finalizing dependencies, ensuring configuration is handled correctly for different environments (dev vs. prod), and creating any necessary build or deployment scripts.

**Acceptance Criteria:**
- All necessary dependencies are listed in `requirements.txt` with appropriate version specifiers.
- Configuration (e.g., Agent Simulator URL, OIDC secrets) is managed in a way suitable for deployment (e.g., using environment variables or Streamlit secrets).
- Any build steps required (if any) are documented or scripted.
- Instructions for deploying the Streamlit app and the Agent Simulator are documented (potentially in the README or a separate DEPLOYMENT.md).
- The application runs correctly using the deployment configuration.

**Estimate:**
2 Story Points

**Dependencies:**
- Finalized codebase and documentation (Task 6.1, 6.3).
- Decision on the deployment target/platform (e.g., Streamlit Community Cloud, Docker, VM).

**Execution Steps:**
1.  Review and finalize the `requirements.txt` file.
2.  Refactor code if necessary to read configuration (like the Agent Simulator URL) from environment variables or Streamlit secrets instead of hardcoding.
3.  Update `.streamlit/secrets.toml` handling or document environment variable setup for production secrets.
4.  Test running the application using environment variables for configuration.
5.  Create simple run scripts (e.g., `run_app.sh`, `run_simulator.sh`) if helpful.
6.  Document the deployment process, including any specific steps for the chosen platform.
7.  Ensure the `.gitignore` file prevents secrets or unnecessary files from being committed.
