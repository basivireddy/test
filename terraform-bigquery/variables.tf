#variables.tf
variable "dataset_id" {
  description = "dataset id"
  type        = string
}
variable "project_id" {
  description = "project id"
  type        = string
}
variable "region" {
  description = "Profile where resources need to be deployed"
  type        = string
}

variable "users" {
    type = list
    description = "list of users"
}