data "aws_iam_policy_document" "lambda_assume_role_policy"{
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    actions = [
      "logs:CreateLogGroup",
    ]
    resources = [
      "*"
    ]
  }
  statement {
    actions = [
      "iam:*",
    ]
    resources = [
      "*"
    ]
  }
  statement {
    actions = [
      "secretsmanager:*",
    ]
    resources = [
      "*"
    ]
  }
  statement {
    actions = [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:us-east-1:*:log-group:/aws/lambda/rotate_iam_credentials:*"
    ]
  }
}

resource "aws_iam_role" "lambda_role" {  
  name = "lambda_role"  
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
  inline_policy {
     name = "lambda_inline_policy"
     policy = data.aws_iam_policy_document.lambda_policy.json
  }
}
