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

variable "hapa_folder_id" {
  description = "Folder ID for Hapa Eikaiwa"
  type        = string
  default     = ""
}

variable "nick_folder_id" {
  description = "Folder ID for Nick Eikaiwa"
  type        = string
  default     = ""
}

variable "life_is_beautiful_folder_id" {
  description = "Folder ID for Life is beautiful"
  type        = string
  default     = ""
}
