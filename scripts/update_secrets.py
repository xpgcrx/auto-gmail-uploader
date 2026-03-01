import os
import subprocess
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# App name prefix defined in Terraform
APP_NAME = "tf-auto-gmail-uploader"

# Map secret IDs to environment variable names
SECRETS = {
    f"{APP_NAME}-client-id": "GCP_CLIENT_ID",
    f"{APP_NAME}-client-secret": "GCP_CLIENT_SECRET",
    f"{APP_NAME}-refresh-token": "GCP_REFRESH_TOKEN",
    f"{APP_NAME}-discord-webhook-url": "DISCORD_WEBHOOK_URL"
}

def set_secret(secret_id: str, value: str, project_id: str) -> None:
    """Use gcloud command to register or update a secret version in Secret Manager."""
    print(f"Setting value for secret: {secret_id} in project: {project_id}...")
    
    # Execute: gcloud secrets versions add [SECRET_ID] --data-file=- --project=[PROJECT_ID]
    process = subprocess.Popen(
        ["gcloud", "secrets", "versions", "add", secret_id, "--data-file=-", f"--project={project_id}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=value)
    
    if process.returncode == 0:
        print(f"Successfully updated {secret_id}.")
    else:
        print(f"Failed to update {secret_id}: {stderr}")

def main() -> None:
    # Project ID for the Google Cloud project
    project_id = "auto-gmail-uploader" 

    for secret_id, env_var in SECRETS.items():
        value = os.environ.get(env_var)
        if value:
            set_secret(secret_id, value, project_id)
        else:
            print(f"Warning: Environment variable {env_var} not found. Skipping...")

if __name__ == "__main__":
    main()
