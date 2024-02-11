terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.47"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.7"
    }
    null = {
      source  = "hashicorp/null"
      version = ">= 3.0"
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