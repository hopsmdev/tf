variable "iam_user_name" {
  type        = string
  description = "IAM User name. It is mandatory to set IAM Use Name"
}

variable "secret_name" {
  type        = string
  default     = "secret"
  description = "AWS Secrets Manager secret name"
}

variable "create_iam_user" {
  type        = bool
  default     = false
  description = "If set true, it will create IAM User with credentials. Disabled by default."
}

variable "rotate_after_days" {
  type        = number
  default     = 30
  description = "It rotates the AWS Secret Manager's secret after N days"
}

variable "enable_rotation" {
  type        = bool
  default     = true
  description = "If set true, it will enable AWS Secret Manager's secret rotation. Enabled by default."
}