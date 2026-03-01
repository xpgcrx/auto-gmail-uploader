# GCP Infrastructure Provisioning for Cloud Functions and Scheduled Jobs

# 1. Service Account Definition
# Create a dedicated identity for the Cloud Function to access Google APIs and Secret Manager.
resource "google_service_account" "service_account" {
  account_id   = "${var.app_name}-sa"
  display_name = "Cloud Functions Service Account (Managed by Terraform)"
}

# 2. Source Code Archiving
# Bundle the application logic, configuration, and dependencies into a single zip file.
data "archive_file" "source" {
  type        = "zip"
  output_path = "source.zip"

  # Place the entry point (main.py) at the root as required by Cloud Functions 2nd gen
  source {
    content  = file("../main.py")
    filename = "main.py"
  }
  # Include requirements.txt to ensure reliable dependency resolution during build
  source {
    content  = file("../requirements.txt")
    filename = "requirements.txt"
  }

  # Logic and configuration directories
  source {
    content  = file("../src/main.py")
    filename = "src/main.py"
  }
  source {
    content  = file("../src/config.py")
    filename = "src/config.py"
  }
  source {
    content  = file("../src/gmail_client.py")
    filename = "src/gmail_client.py"
  }
  source {
    content  = file("../src/drive_client.py")
    filename = "src/drive_client.py"
  }
  source {
    content  = file("../src/converter.py")
    filename = "src/converter.py"
  }
  source {
    content  = file("../src/notifier.py")
    filename = "src/notifier.py"
  }
  source {
    content  = file("../configs/newsletters.yaml")
    filename = "configs/newsletters.yaml"
  }
}

# 3. Storage Bucket for Source Code
# Create a GCS bucket to temporarily store the zip archive for deployment.
resource "google_storage_bucket" "bucket" {
  name                        = "${var.project_id}-source-bucket-tf"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true # Allow bucket deletion during project teardown
}

# 4. Upload Zip to Storage
# Upload the source archive to the GCS bucket. 
# Re-deployment is triggered automatically whenever the file hash changes.
resource "google_storage_bucket_object" "zip" {
  name   = "source-${data.archive_file.source.output_md5}.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.source.output_path
}

# 5. Cloud Functions (2nd gen) Definition
# The actual execution environment for the Python application.
resource "google_cloudfunctions2_function" "function" {
  name        = var.app_name
  location    = var.region
  description = "Automatically upload Gmail newsletters to Google Drive (Terraform)"

  build_config {
    runtime     = "python312"
    entry_point = "main" # Calls the main function in main.py
    # Use the dedicated SA for build access to the source bucket
    service_account = google_service_account.service_account.id
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.zip.name
      }
    }
  }

  service_config {
    max_instance_count    = 1     # Limit concurrency to control costs
    available_memory      = "256Mi"
    timeout_seconds       = 60
    service_account_email = google_service_account.service_account.email
    
    # Map Secret Manager secrets to environment variables for secure access in code
    secret_environment_variables {
      key        = "GCP_CLIENT_ID"
      project_id = var.project_id
      secret     = google_secret_manager_secret.gcp_client_id.secret_id
      version    = "latest"
    }
    secret_environment_variables {
      key        = "GCP_CLIENT_SECRET"
      project_id = var.project_id
      secret     = google_secret_manager_secret.gcp_client_secret.secret_id
      version    = "latest"
    }
    secret_environment_variables {
      key        = "GCP_REFRESH_TOKEN"
      project_id = var.project_id
      secret     = google_secret_manager_secret.gcp_refresh_token.secret_id
      version    = "latest"
    }
    secret_environment_variables {
      key        = "DISCORD_WEBHOOK_URL"
      project_id = var.project_id
      secret     = google_secret_manager_secret.discord_webhook_url.secret_id
      version    = "latest"
    }
  }
}

# 6. Cloud Scheduler Configuration
# Defines a periodic trigger (e.g., every hour) to execute the Cloud Function.
resource "google_cloud_scheduler_job" "job" {
  name        = "${var.app_name}-scheduler"
  description = "Hourly Gmail polling and upload (Terraform)"
  schedule    = "0 * * * *" # Cron syntax: every hour on the hour
  region      = var.region

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.function.url
    
    # Authenticate requests using the service account's OIDC token
    oidc_token {
      service_account_email = google_service_account.service_account.email
    }
  }
}

# 7. IAM Permissions
# Grant the service account necessary permissions to interact with project resources.

# Project-level Storage Viewer (required for accessing build-time source buckets)
resource "google_project_iam_member" "storage_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

# Artifact Registry Writer (required for storing built container images)
resource "google_project_iam_member" "artifact_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

# Secret Manager Secret Accessor (required for retrieving sensitive credentials)
resource "google_project_iam_member" "secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

# Cloud Functions Invoker (required for Scheduler to trigger the function)
resource "google_cloudfunctions2_function_iam_member" "invoker" {
  project        = google_cloudfunctions2_function.function.project
  location       = google_cloudfunctions2_function.function.location
  cloud_function = google_cloudfunctions2_function.function.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${google_service_account.service_account.email}"
}

# Cloud Run Invoker (required as 2nd gen functions run internally on Cloud Run)
resource "google_cloud_run_service_iam_member" "run_invoker" {
  project  = google_cloudfunctions2_function.function.project
  location = google_cloudfunctions2_function.function.location
  service  = google_cloudfunctions2_function.function.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.service_account.email}"
}
