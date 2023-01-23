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