locals {
  name            = "eks-${replace(basename(path.cwd), "_", "-")}"
  cluster_version = "1.31"
  region          = "us-east-2"

  vpc_cidr = "10.0.0.0/16"
  azs      = slice(data.aws_availability_zones.available.names, 0, 3)

  tags = {
    Name    = local.name
    GithubRepo = "terraform-aws-eks"
    GithubOrg  = "terraform-aws-modules"
  }
}
data "aws_availability_zones" "available" {}

