# auto-gmail-uploader Development Guidelines

## Tech Stack

- **Language**: Python 3.12+
- **Package Management**: `uv`
- **Infrastructure**: Google Cloud Functions, Cloud Scheduler
- **IaC**: Terraform

## Coding Conventions

1. **Type Hints**
   - All functions and methods must include type hints.
   - Example: `def fetch_emails(query: str) -> list[dict]:`
2. **Formatting and Linting**
   - Follow standard Python formatting (using tools like `ruff` if configured).
3. **Error Handling**
   - Always use `try...except` blocks when calling external APIs (Gmail, Drive, Discord) with proper logging.
   - Failures must be notified via Discord Webhook with detailed error information.

## Critical Security Rules

- **No Hardcoded Secrets**: Never hardcode `CLIENT_ID`, `CLIENT_SECRET`, `REFRESH_TOKEN`, or `DISCORD_WEBHOOK_URL` in source code or config files.
- **Git Exclusion**: Local credential files like `client_secret.json` must be included in `.gitignore` and never committed.
- All secrets must be dynamically retrieved from Google Cloud Secret Manager in the production environment.

## Running Tests

- Use `pytest` as the test runner.
- **Command**: `uv run python -m pytest`
- Mock external API dependencies (`unittest.mock`) to ensure tests can run independently in local environments.
