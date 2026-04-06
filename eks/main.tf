module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version
  vpc_id          = var.vpc_id
  subnet_ids      = var.subnet_ids


  create_cloudwatch_log_group = false

  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    group_one = {
      instance_types = ["t3.small"]
      min_size = 1 
      max_size = 2 
      desired_size = 1
    }
    group_two = {
      instance_types = ["t3.small"]
      min_size = 1 
      max_size = 2 
      desired_size = 1
    }
  }
}