terraform {
  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.10.0"
    }
  }
}

provider "helm" {
  kubernetes {
    host                   = data.terraform_remote_state.eks.outputs.cluster_endpoint
    cluster_ca_certificate = base64decode(data.terraform_remote_state.eks.outputs.cluster_certificate_authority_data)

    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", data.terraform_remote_state.eks.outputs.cluster_name]
      command     = "aws"
    }
  }
}

data "terraform_remote_state" "eks" {
  backend = "local"
  config = {
    # Перевірте, чи цей шлях вірно веде до вашої папки з EKS
    path = "../../leson5/terraform.tfstate" 
  }
}