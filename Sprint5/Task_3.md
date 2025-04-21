# Sprint 5 - Task 5.3: Email-Based Access Control Implementation

**Description:**
Implement email-based access control within the application using our existing Google authentication. Based on the authenticated user's email address, the Agent Simulator will tailor the UI specification, showing different elements and capabilities depending on whether the user is an admin or a regular user.

**Acceptance Criteria:**
- The authenticated user's email (obtained during Google login) is used to determine their access level
- Two specific test emails are supported with different access levels:
  - `feloes@gmail.com` → Admin access (full capabilities)
  - `fede@urobora.com` → Regular user access (limited capabilities)
- The user's email is sent to the Agent Simulator with all requests
- Agent Simulator modifies the UI specification based on the user's email
- Admin users see additional UI elements and have access to more features
- Regular users see a simplified interface with restricted capabilities
- Unauthorized actions are prevented for regular users

**Estimate:**
4 Story Points

**Dependencies:**
- Completion of Sprint 4 tasks (Google Authentication)
- Working Agent Simulator with basic functionality

**Execution Steps:**
1. Define two access levels with specific capabilities:
   - Admin (feloes@gmail.com): Full access to all features
   - Regular User (fede@urobora.com): Limited access to basic features

2. Update the Streamlit app to extract and store the user's email in session state after login

3. Modify API calls to the Agent Simulator to include the user's email address

4. Enhance the Agent Simulator to check the email and determine the appropriate access level

5. Implement logic in the Agent Simulator to customize UI specifications based on the user's access level:
   - For Admin users: Include advanced features, configuration options, and administrative tools
   - For Regular users: Show only basic features and hide administrative capabilities

6. Create a new UI specification (SPEC_V6) that demonstrates different views based on user access level

7. Add visual indicators in the UI to show the current user's access level

8. Test the implementation by logging in with both test email addresses and verifying that:
   - Each user sees the appropriate UI elements
   - Restricted actions are properly prevented for regular users
   - The experience is seamless and intuitive for both user types
