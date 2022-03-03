terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
  access_key = ""
  secret_key = ""


}


resource "aws_s3_account_public_access_block" "example" {
  block_public_acls   = true
  block_public_policy = true
}

resource "aws_s3_bucket" "mybucket" {
  bucket = "twinkiestatebucket12233444444"

}

resource "aws_s3_bucket_server_side_encryption_configuration" "s3_encryption_configuration" {
  bucket = aws_s3_bucket.mybucket.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
    }
  }
}
