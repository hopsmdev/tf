# Example 1
# Create new IAM User `MyUser` with credentials rotated every 7 days (rotation automatically enabled)

module "aws-iam-credentials-rotation" {
  source            = "./aws-iam-credentials-rotation"
  iam_user_name     = "MyUser"
  create_iam_user   = true     # Default is False
  rotate_after_days = 7        # Default is 30 days
  enable_rotation   = true     # Default is True
}

# Example 2
# Create new IAM User `MyUser` with credentials rotated every 7 days (rotation disabled)
# It creates lambda function, secrets manager's secret, iam user, iam user credentials
# but lambda function to rotate credentials will not be executed automatically 

module "aws-iam-credentials-rotation" {
  source            = "./aws-iam-credentials-rotation"
  iam_user_name     = "MyUser"
  create_iam_user   = true     # Default is False
  rotate_after_days = 7        # Default is 30 days
  enable_rotation   = false    # Default is True
}

# Example 3
# Rotate IAM Credentials (default after 30 days) for an existing IAM user
# It stores IAM Credentials in Secrets Manager's `secret` secret (by default)

module "aws-iam-credentials-rotation" {
  source            = "./aws-iam-credentials-rotation"
  iam_user_name     = "MyUser"
}

# Example 4
# Rotate IAM Credentials (default after 30 days) for an existing IAM user
# It stores IAM Credentials in Secrets Manager's `MySecret` secret

module "aws-iam-credentials-rotation" {
  source            = "./aws-iam-credentials-rotation"
  iam_user_name     = "MyUser"
  secret_name       = "MySecret"
}