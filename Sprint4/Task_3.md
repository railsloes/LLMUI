# Issue 4.3: Configure Streamlit Secrets (secrets.toml)

## Description
Create/update .streamlit/secrets.toml with the [auth] section (redirect_uri, cookie_secret) and provider sections ([auth.providers.google], [auth.providers.microsoft]) including client IDs/secrets and metadata URLs. Ensure file is gitignored.

## Acceptance Criteria
- secrets.toml correctly configured for both providers
- cookie_secret is a strong random string
- File is not in Git

## Estimate
Small

## Dependencies
- Issues 4.1, 4.2

## Execution Steps
1. Create the directory if it doesn't exist: `mkdir .streamlit`
2. Create the file: `touch .streamlit/secrets.toml`
3. Generate a strong secret (e.g., run `openssl rand -hex 32` in your terminal and copy the output)
4. Add the content to secrets.toml, replacing placeholders with your actual credentials and the generated cookie secret:
```toml
# .streamlit/secrets.toml
[auth]
redirect_uri = "http://localhost:8501" # MUST match registration in IdP
cookie_secret = "PASTE_YOUR_STRONG_RANDOM_32_BYTE_HEX_SECRET_HERE"

[auth.providers.google]
client_id = "PASTE_YOUR_GOOGLE_CLIENT_ID_HERE"
client_secret = "PASTE_YOUR_GOOGLE_CLIENT_SECRET_HERE"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

[auth.providers.microsoft]
client_id = "PASTE_YOUR_MICROSOFT_CLIENT_ID_HERE"
client_secret = "PASTE_YOUR_MICROSOFT_CLIENT_SECRET_HERE"
# Use 'common' for multi-tenant/MSA, or your specific tenant ID
server_metadata_url = "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"
```

5. Ensure .streamlit/secrets.toml is listed in your .gitignore file
