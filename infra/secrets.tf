# Secret Manager Definitions

# 1. OAuth Client ID
resource "google_secret_manager_secret" "gcp_client_id" {
  secret_id = "${var.app_name}-client-id"
  replication {
    auto {}
  }
}

# 2. OAuth Client Secret
resource "google_secret_manager_secret" "gcp_client_secret" {
  secret_id = "${var.app_name}-client-secret"
  replication {
    auto {}
  }
}

# 3. Refresh Token
resource "google_secret_manager_secret" "gcp_refresh_token" {
  secret_id = "${var.app_name}-refresh-token"
  replication {
    auto {}
  }
}

# 4. Discord Webhook URL
resource "google_secret_manager_secret" "discord_webhook_url" {
  secret_id = "${var.app_name}-discord-webhook-url"
  replication {
    auto {}
  }
}
