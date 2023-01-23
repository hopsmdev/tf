# Example 3
# Rotate IAM Credentials (default after 30 days) for an existing IAM user
# It stores IAM Credentials in Secrets Manager's `secret` secret (by default)

module "aws-iam-credentials-rotation" {
  iam_user_name     = "MyUser"
}
