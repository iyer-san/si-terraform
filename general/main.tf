terraform {

  required_providers {
   aws = {
     source  = "hashicorp/aws"
     version = "~> 4.66.1"
   }
 }

  backend "s3" {
    bucket         = "general-terraform-state-use2"
    key            = "terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "general-terraform-state-table-use2"
    profile = "si-iamadmin-general"
  }
}
provider "aws" {
    region = "us-east-2"
    profile = "si-iamadmin-general"
}

resource "aws_s3_bucket" "example-bucket" {
  bucket = "si-general-example-bucket"

  tags = {
    Name        = "si-general-example-bucket"
    Environment = "general"
  }
}