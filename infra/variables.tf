variable "region" {
  type    = string
  default = "us-east-1"
}

variable "prefix" {
  type    = string
  default = "youtube"
}

variable "s3_bucket_name" {
  type = string
  default = "my-youtube-bucket"
}
