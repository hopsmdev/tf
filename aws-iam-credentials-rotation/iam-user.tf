resource "aws_iam_user" "iam_user" {
    count         = var.create_iam_user == true ? 1 : 0
    name          = var.iam_user_name
    force_destroy = true
}

resource "aws_iam_access_key" "iam_user_credentials" {
  user = aws_iam_user.iam_user[0].name
}