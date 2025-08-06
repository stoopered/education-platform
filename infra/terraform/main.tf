terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# S3 buckets
resource "aws_s3_bucket" "website" {
  bucket = var.website_bucket_name
  acl    = "public-read"
  website {
    index_document = "index.html"
  }
}

resource "aws_s3_bucket" "assets" {
  bucket = var.assets_bucket_name
  versioning {
    enabled = true
  }
}

# DynamoDB table
resource "aws_dynamodb_table" "student_progress" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "studentId"
  range_key    = "timestamp"
  attribute {
    name = "studentId"
    type = "S"
  }
  attribute {
    name = "timestamp"
    type = "S"
  }
}

# Cognito user pool
resource "aws_cognito_user_pool" "main" {
  name = var.user_pool_name
  auto_verified_attributes = ["email"]
  password_policy {
    minimum_length    = 8
    require_lowercase = false
    require_uppercase = false
    require_numbers   = false
    require_symbols   = false
  }
}

resource "aws_cognito_user_pool_client" "web" {
  name         = "${var.user_pool_name}-client"
  user_pool_id = aws_cognito_user_pool.main.id
  generate_secret = false
}

# Note: Complete Lambda and API Gateway resources can be added using the
# `aws_lambda_function` and `aws_apigatewayv2_*` resources.  For brevity this
# skeleton omits the full configuration.

variable "region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "website_bucket_name" {
  type        = string
  default     = "education-platform-website-${random_id.suffix.hex}"
}

variable "assets_bucket_name" {
  type        = string
  default     = "education-platform-assets-${random_id.suffix.hex}"
}

variable "dynamodb_table_name" {
  type        = string
  default     = "education-platform-progress"
}

variable "user_pool_name" {
  type        = string
  default     = "education-platform-user-pool"
}

resource "random_id" "suffix" {
  byte_length = 4
}