variable "iam_user_name" {
  type        = string
  description = "IAM User name"
}

variable "secret_name" {
  type        = string
  default     = "secret"
  description = "AWS Secrets Manager secret name"
}