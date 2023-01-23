# Example 4
# Rotate IAM Credentials (default after 30 days) for an existing IAM user
# It stores IAM Credentials in Secrets Manager's `MySecret` secret

module "aws-iam-credentials-rotation" {
  iam_user_name     = "MyUser"
  secret_name       = "MySecret"
}