resource "aws_secretsmanager_secret" "secretsmanager_secret" {
  name_prefix  = var.secret_name
}

resource "aws_secretsmanager_secret_rotation" "secretsmanager_secret_rotation" {
  count               = var.enable_rotation == true ? 1 : 0
  secret_id           = aws_secretsmanager_secret.secretsmanager_secret.id
  rotation_lambda_arn = aws_lambda_function.rotate_iam_credentials.arn

  rotation_rules {
    automatically_after_days = var.rotate_after_days
  }
}
 
resource "aws_secretsmanager_secret_version" "secret_version" {
  secret_id = aws_secretsmanager_secret.secretsmanager_secret.id
  secret_string = <<EOF
   {
    "access_key": "placeholder",
    "secret_key": "pleaceholder"
   }
EOF
}
 
# Importing the AWS secrets created previously using arn.
data "aws_secretsmanager_secret" "secretsmanager_secret" {
  arn = aws_secretsmanager_secret.secretsmanager_secret.arn
}