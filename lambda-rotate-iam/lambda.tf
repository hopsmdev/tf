data "archive_file" "python_lambda_package" {  
  type = "zip"  
  source_file = "${path.module}/lambda/rotate_iam_credentials.py" 
  output_path = "rotate_iam_credentials.zip"
}

resource "aws_lambda_function" "rotate_iam_credentials" {
        function_name = "rotate_iam_credentials"
        filename      = "rotate_iam_credentials.zip"
        source_code_hash = data.archive_file.python_lambda_package.output_base64sha256
        role          = aws_iam_role.lambda_role.arn
        runtime       = "python3.9"
        handler       = "rotate_iam_credentials.lambda_handler"
        timeout       = 10

        environment {
            variables = {
                IAM_USER_NAME = var.iam_user_name
            }
        }
}

resource "aws_lambda_permission" "allow_secrets_manager" {
    statement_id = "AllowExecutionFromSecretsManager"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.rotate_iam_credentials.function_name
    principal = "secretsmanager.amazonaws.com"
}