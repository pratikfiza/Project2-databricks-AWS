terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  required_version = ">= 1.0.0"
}

provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "data" {
  bucket = var.s3_bucket_name
  acl    = "private"
}

resource "aws_kinesis_stream" "youtube_stream" {
  name        = "${var.prefix}-youtube-stream"
  shard_count = 1
}

resource "aws_dynamodb_table" "metadata" {
  name         = "${var.prefix}-metadata"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "event_id"
  attribute {
    name = "event_id"
    type = "S"
  }
}

resource "aws_sns_topic" "alerts" {
  name = "${var.prefix}-alerts"
}

output "s3_bucket" {
  value = aws_s3_bucket.data.id
}
