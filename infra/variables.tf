variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Region to deploy resources"
  type        = string
  default     = "us-central1" # Recommended region for Google Cloud Free Tier
}

variable "app_name" {
  description = "Application name prefix"
  type        = string
  default     = "tf-auto-gmail-uploader"
}
