#providers.tf
terraform {
#    required_version = "~> 1.2.1"
    required_providers {
        google = ">=2.7, <5.0"
        google-beta = ">=2.7, <5.0"
    }
}

provider "google" {
    project = var.project_id
}

provider "google-beta" {
    project = var.project_id
}