# Example 1
# Create new IAM User `MyUser` with credentials rotated every 7 days (rotation automatically enabled)

module "aws-iam-credentials-rotation" {
  source            = "./aws-iam-credentials-rotation"
  iam_user_name     = "MyUser"
  create_iam_user   = true     # Default is False
  rotate_after_days = 7        # Default is 30 days
  enable_rotation   = true     # Default is True
}